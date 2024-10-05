
from django.shortcuts import render
from . models import *
from django.views.generic import ListView
# Create your views here.


class ShowAllProfilesView(ListView):
    ''' a view to show all Profiles from template html file show_all_profiles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'