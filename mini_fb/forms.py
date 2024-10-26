from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    ''' CreateProfileForm used to create Profile Model data'''
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email_address = forms.EmailField(label="Email", required=True)
    profile_image_url = forms.URLField(label="Profile Image URL", required=True)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2012,1920,-1),), required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']
        
class CreateStatusMessageForm(forms.ModelForm):
     ''' CreateStatusMessageForm used to create StatusMessage Model data'''
     message = forms.CharField(label="Message", required=True)
     
     class Meta:
         model = StatusMessage
         fields = ['message']
         
class UpdateProfileForm(forms.ModelForm):
    ''' Form to update a Profile '''
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']
        