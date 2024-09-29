from django.urls import path
from django.conf import settings
from . import views

# create list of URLs for app:
urlpatterns:list = [
    
    
    # URL for the home page, mapped to /
    path('', views.main, name="main"),
    
    # URL for the quotes page, mapped to /confirmation/
    path('confirmation/', views.confirmation, name="confirmation"),
    
    # URL for the show all page, mapped to /order/
    path('order/', views.order, name='order'),
]
