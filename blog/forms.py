# blog/forms.py

from django import forms
from .models import Comment


class CreateCommentForm(forms.models):
    '''A form to create Comment data.'''
    class Meta:
        
        ''' associate this form with the Comment model'''
        model = Comment
        field = ['article', 'author', 'text']
    
