# project/urls.py

# description: the app-specific URLS for the PetMate application


from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# create list of URLs for PetMate app:

urlpatterns =  [
    # Home page
    path("", views.HomePage.as_view(), name="index"),
    
    # Authentication 
    #_______________________________________________________________
    # Route for Login to PetMate with username and password
    path("login/", auth_views.LoginView.as_view(template_name='project/login.html'), name="login"),
    # Route for Logout of PetMate application
    path("logout/", 
    auth_views.LogoutView.as_view(next_page='index', template_name='project/login.html'), 
    name="logout"),
    path('register/', views.RegisterView.as_view(template_name='project/register.html'), name='register'),
    #_______________________________________________________________
    
    # Shelter
    #_______________________________________________________________
    # Route to view all Shelters
    path("shelters/", views.ShowSheltersPage.as_view(), name="shelters"),
    # Route to view a specific Shelter by ID
    path("shelters/<int:pk>/", views.ShowShelterPage.as_view(), name="shelter"),
    #_______________________________________________________________
     
    # Pets Routes
    #_______________________________________________________________
    # Route to view all Pets
    path("pets/", views.ShowPetsPage.as_view(), name="pets"),
    # Route to view a specific Pet by ID
    path("pets/<int:pk>/", views.ShowPetPage.as_view(), name="pet"),
    #_______________________________________________________________
    
    # Adoption Routes
    #_______________________________________________________________
    # Route for Shelters to View all adoptions
    path("adoptions/", views.ViewAdoptionPage.as_view(), name="view_adoptions"),
    # Route for pet owners to adopt a Pet
    path("adoptions/<int:pet_id>/", views.CreateAdoptionPage.as_view(), name="view_adoption"),
    #_______________________________________________________________
    
    # Adoption View Routes
    #_______________________________________________________________
    # Route for pet owners to view their adoptions
    path("my_adoptions/", views.ViewMyAdoptionsPage.as_view(), name="view_my_adoptions"),
    # Route for pet owners to view their adoptions
    path("my_adoptions/<int:adoption_id>/", views.ViewMyAdoptionPage.as_view(), name="view_my_adoption"),
    
    path("adoptions/<int:adoption_id>/cancel/", views.DeleteAdoptionRequestView.as_view(), name="cancel_adoption"),
    #_______________________________________________________________
      
    # Comment Routes
    #_______________________________________________________________
    # Route for Users to comment on Pet profile 
    path("comments/create/<int:pet_id>/", views.CreateCommentView.as_view(), name="create_comment"),
    # Route for Users to edit comments on Pet profile 
    path('comments/<int:pk>/edit/', views.UpdateCommentView.as_view(), name='edit_comment'),
     # Route for Users to delete comments on Pet profile 
    path("comments/delete/<int:pk>/", views.DeleteCommentView.as_view(), name="delete_comment"),
    #_______________________________________________________________
    
    # Filtering Routes
    #_______________________________________________________________
    # Route used for filtering pet profiles based on pet name or age/breed
    path("pets/search/", views.FilterPetPage.as_view(), name="pet_search"),
    # Route used for filtering shelter profiles based of Shelter name
    path("shelters/search/", views.FilterShelterPage.as_view(), name="shelter_search"),
    #_______________________________________________________________
     
    # Shelter Review Routes
    #_______________________________________________________________
    # Route to create a review for a shelter
    path("shelters/<int:shelter_id>/reviews/create/", 
         views.CreateShelterReviewView.as_view(), 
         name="create_shelter_review"),
    # Route to update a review
    path("reviews/<int:pk>/update/", 
         views.UpdateShelterReviewView.as_view(), 
         name="update_shelter_review"),
    # Route to delete a review
    path("reviews/<int:pk>/delete/", 
         views.DeleteShelterReviewView.as_view(), 
         name="delete_shelter_review"),
    #_______________________________________________________________
]