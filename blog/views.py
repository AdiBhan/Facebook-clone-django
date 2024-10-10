# blogs/views.py
# views to show the blog application
from django.shortcuts import render
from . models import *
from django.views.generic import ListView, CreateView, DetailView
from .forms import *
# Create your views here.

class ShowAllViews(ListView):
    ''' a video to show all Articles'''
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'
    
class RandomArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    # pick one article at random:
    def get_object(self):
        '''Return one Article object chosen at random.'''
        all_articles = Article.objects.all()
        return random.choice(all_articles)
class CreateCommentsView(CreateView):
    '''A view to show/process the create comment form'''
    
    form_class = CreateCommentForm
    template_name = "create_comment_form.html"