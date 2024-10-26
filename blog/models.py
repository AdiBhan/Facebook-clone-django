# blog/models.py
from django.db import models

# Create your models here.

class Article(models.Model):
    '''Article Class'''
    
    
    # data attributes:
    
    text = models.TextField(blank=False)
    author = models.TextField(blank=False)
    title = models.TextField(blank=False)
    published = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True)
    
    
    def __str__(self):
        '''Returns a string representation of this Article'''
        return f"{self.title} by {self.author}"
    
    def get_comments(self):
        ''' Return a list of comments'''
        
        # Use the ORM to filter comments where this object is the Foreign Key
        
        comments = Comment.objects.filter(article=self)
        return comments
    
    
class Comment(models.Model):
    ''' Encapsulates a comment on an article'''
    
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        ''' Return a string representation of this object'''
        
        return f"{self.article}"
    
