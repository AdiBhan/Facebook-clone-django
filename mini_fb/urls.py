from django.urls import path
from django.conf import settings
from . import views


# create list of URLs for app:
urlpatterns = [
   ## Class based view to show all profiles and display the show_all.html template
   path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
   # Class based view to search based on path query parameters for a specific profile
   path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
   # Class based view to create a new profile
    path('create_profile', views.CreateProfileView.as_view(), name='create_profile'),
     # Class based view to create a new status message
    path('profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name='create_status'),
      # Class-based view to update a profile
   path('profile/<int:pk>/update', views.UpdateProfileView.as_view(), name='update_profile'),
   path('status/<int:pk>/delete/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),
   
]
