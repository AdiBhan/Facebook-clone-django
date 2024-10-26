# blogs/views.py
# views to show the blog application
from django.shortcuts import render
from django.urls import reverse
from .models import Article 
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from .forms import CreateCommentForm
import random

# Create your views here.


    # ListView shows all of the Articles
class ShowAllViews(ListView):
    ''' a video to show all Articles'''
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'
    
    
    # Detail views picks "one" of the Articles (one record)
class ArticleView(DetailView):
    ''' Show a random article'''
    
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    
    
    # Error: Generic detail view RandomArticleView must be called with either an object pk or a slug in the URLconf.
    # Solution: Must implement method get_object
    
    def get_object(self): 
        ''' returns random record/ object of Articles'''
        
        all_articles = Article.objects.all()
        return random.choice(all_articles) 
        
class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
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