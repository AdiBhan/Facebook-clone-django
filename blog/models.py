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