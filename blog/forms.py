## let's solve the "which Article" part more elegantly:
# 1 - remove article from the form fields
# blog/forms.py
from django import forms
from .models import Comment
class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields'''
        model = Comment
        fields = ['author', 'text', ]  # which fields from model should we use
