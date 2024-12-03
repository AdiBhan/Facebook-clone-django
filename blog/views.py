# blogs/views.py
# views to show the blog application
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Article 
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from .forms import CreateCommentForm
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateArticleForm  
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm 
# Create your views here.


    # ListView shows all of the Articles
class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Article # retrieve objects of type Article from the database
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # how to find the data in the template file
    def dispatch(self, request):
        '''add this method to show/debug logged in user'''
        print(f"Logged in user: request.user={request.user}")
        print(f"Logged in user: request.user.is_authenticated={request.user.is_authenticated}")
        return super().dispatch(request)
    
    
    # Detail views picks "one" of the Articles (one record)
class ArticleView(DetailView):
    ''' Show a random article'''
    
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    
    
    # Error: Generic detail view RandomArticleView must be called with either an object pk or a slug in the URLconf.
    # Solution: Must implement method get_object
    
    def get_object(self):
        ''' Returns a random record/object of Articles or raises 404 if none exist '''
        all_articles = Article.objects.all()
        print(all_articles)
        if not all_articles:
            # Raise a 404 error if no articles are available
            raise Http404("No articles available")
        return random.choice(all_articles)
    
        
class CreateCommentView(LoginRequiredMixin, CreateView):
    '''A view to create a new comment and save it to the database.'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
    login_url = "/blog/login"
    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Article to the Comment object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        
        # Find the article with the PK from the URL
        article = Article.objects.get(pk=self.kwargs['pk'])
        # print(article)
        
        # Attach the article
        # 
        # to the new Comment
        form.instance.article = article
        
        return super().form_valid(form)
    

## also:  revise the get_success_url
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        return reverse('article', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        ''' Build the dict of key-value pairs that become context variables within the template'''
        return super().get_context_data(**kwargs)
    

class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to create a new Article and save it to the database.'''
    form_class = CreateArticleForm  # Assign the CreateArticleForm to form_class
    template_name = "blog/create_article_form.html"
    login_url = "/blog/login"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")
        # attach user to form instance (Article object):
        form.instance.user = user
        return super().form_valid(form)
    template_name = "blog/create_article_form.html"
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    

    
# The commented out `RegistrationView` class in the `views.py` file is a view that is intended to
# handle the form submission for account registration. It is using a `CreateView` which is a generic
# view provided by Django to handle the creation of objects.

class RegistrationView(CreateView):
    '''
    Show/process form for account registration
    '''
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    success_url = '/blog/'

    def dispatch(self, request, *args, **kwargs):
        # Common logic for all requests
        print("Dispatch called")
        print(f"Request method: {request.method}")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Specific logic for GET requests
        print("GET called: Initial page load")
        self.object = None  # Required for CreateView to render a blank form
        context = self.get_context_data()
        context['example_variable'] = "Welcome to Registration!"
        return self.render_to_response(context)

    def form_valid(self, form):
        # Specific logic for successful POST requests
        user = form.save()
        login(self.request, user)
        print(f"User created: {user}")
        return redirect(self.success_url)
