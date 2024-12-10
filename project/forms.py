# project/forms.py


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Pet, User, Comment, ShelterReview, AdoptionRequest

class CommentForm(forms.ModelForm):
    '''CommentForm renders a form with a 'content' TextArea field where users can write out and type comments'''
    class Meta:
        model = Comment   ## CommentForm based on the comment model
        fields = ['content']  # fields we need access too
        widgets = {  ## JSON object/Dictionary with each field and the corresponding widget
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }

class ShelterReviewForm(forms.ModelForm):
    '''ShelterReviewForm renders a form with:
        1. 'rating' input field where users can select between 1-5 overall rating for the shelter
        2. a 'review_text' TextArea field where users can give more in-depth feedback to the shelter'''
    class Meta:
        model = ShelterReview
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'rating-input'
            }),
            'review_text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your review here...'
            })
        }

class AdoptionRequestForm(forms.ModelForm):
    '''AdoptionRequestForm renders a form that allows users to submit adoption requests with:
        1. A 'notes' TextArea field where potential adopters can explain why they would be good pet parents
        This form is used in the adoption application process'''
    class Meta:
        model = AdoptionRequest   ## AdoptionRequestForm based on the AdoptionRequest model
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Please explain why you would be a good pet parent...'
            })
        }

class PetSearchForm(forms.Form):
    '''PetSearchForm provides a search interface for pets with:
        1. A text search field for general queries
        2. A pet type filter dropdown using predefined PET_TYPES
        3. A maximum age filter for finding pets under a specific age
        This form helps users narrow down pet listings based on their preferences'''
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search pets...'})
    )
    pet_type = forms.ChoiceField(
        choices=[('', 'All')] + Pet.PET_TYPES,
        required=False
    )
    max_age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'min': 0, 'placeholder': 'Maximum age'})
    )

class ShelterSearchForm(forms.Form):
    '''ShelterSearchForm enables users to search for shelters with:
        1. A text search field for shelter names
        2. A location field to find nearby shelters
        3. A minimum rating filter to find highly-rated shelters
        This form helps users find shelters that match their criteria and location preferences'''
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search shelters...'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Location'})
    )
    min_rating = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'min': 1,
            'max': 5,
            'placeholder': 'Minimum rating'
        })
    )

class UserRegistrationForm(UserCreationForm):
    '''UserRegistrationForm extends Django's UserCreationForm to handle user registration with:
        1. Username field
        2. Email field (required)
        3. Password fields with confirmation
        Includes custom email validation to prevent duplicate registrations'''
    email = forms.EmailField(required=True)
    class Meta:
        model = User  #
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        '''clean_email() method validates that the email isn't already registered in the system'''
        
        email = self.cleaned_data.get('email') # get email address of user
        if User.objects.filter(email=email).exists(): # If email is already associated with a user, raise error
            raise forms.ValidationError("This email is already registered.")
        return email # else return email