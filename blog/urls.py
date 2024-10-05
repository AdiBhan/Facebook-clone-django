# blog/urls.py
# description: the app-specific URLS for the HW application


from django.urls import path
from django.conf import settings
from . import views


# create list of URLs for app:
urlpatterns = [
   
   path('', views.ShowAllViews.as_view(), name='show_all'),
   
]
