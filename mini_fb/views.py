
from django.shortcuts import render
from . models import *
from django.views.generic import ListView
# Create your views here.


class ShowAllProfilesView(ListView):
    ''' a view to show all Profiles from template html file show_all_profiles'''
    model = Profile ## references model found in models.py
    template_name = 'mini_fb/show_all_profiles.html'  # references HTML webpage to display UI of webpage found in templates/mini_fb/show_all.html
    context_object_name = 'profiles' # profiles references the actual DB table which we can use in the HTML page to display records