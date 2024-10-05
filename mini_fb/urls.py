from django.urls import path
from django.conf import settings
from . import views


# create list of URLs for app:
urlpatterns = [
   ## Class based view to show all profiles and display the show_all.html template
   path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
   
]
