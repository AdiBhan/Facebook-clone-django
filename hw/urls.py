# hw/urls.py
# description: the app-specific URLS for the HW application


from django.urls import path
from django.conf import settings
from . import views


# create list of URLs for app:
urlpatterns = [
    # URL for the home page, mapped to /hw/
    path('', views.home, name="home"),
    # URL for the about page, mapped to /hw/about/
    path('about/', views.about, name="about"),
]
