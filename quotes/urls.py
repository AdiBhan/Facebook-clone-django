# hw/urls.py
# description: the app-specific URLS for the HW application


from django.urls import path
from django.conf import settings
from . import views


# create list of URLs for app:
urlpatterns:list = [
    
    
    # URL for the home page, mapped to /
    path('', views.index, name="index"),
    
    # URL for the quotes page, mapped to /quote/
    path('quote/', views.quote, name="quote"),
    
    # URL for the show all page, mapped to /show_all/
    path('show_all/', views.show_all, name='show_all'),
    
    # URL for the about page, mapped to /about/
    path('about/', views.about, name="about")
    
    
]
