from django import forms
from .models import ShelterReview



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Shelter, Pet, User, Comment, ShelterReview, AdoptionRequest

class ShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'address', 'contact_info', 'location', 'capacity', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'contact_info': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity < 0:
            raise forms.ValidationError("Capacity cannot be negative")
        return capacity

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'age', 'breed', 'image', 'pet_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'pet_type': forms.Select(choices=Pet.PET_TYPES),
            'age': forms.NumberInput(attrs={'min': 0}),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 0:
            raise forms.ValidationError("Age cannot be negative")
        return age

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_shelter_employee = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_shelter_employee']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }

class ShelterReviewForm(forms.ModelForm):
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

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5")
        return rating

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Please explain why you would be a good pet parent...'
            })
        }

class PetSearchForm(forms.Form):
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
    
    
class ShelterReviewForm(forms.ModelForm):
    class Meta:
        model = ShelterReview
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review_text': forms.Textarea(attrs={'rows': 4}),
        }