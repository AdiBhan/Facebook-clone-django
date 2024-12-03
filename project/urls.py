# project/urls.py

# description: the app-specific URLS for the PetMate application


from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# create list of URLs for PetMate app:

urlpatterns =  [
    
    # Route for Login to PetMate with username and password
    path("/login/", auth_views.LoginView.as_view()),
    # Route for Logout of PetMate application
    path("/logout/", auth_views.LogoutView.as_view()),
    
    
    # Route to view all Shelters
    path("/shelters/", views.ShowSheltersPage.as_view(), name="shelters"),
    
    
    # Route to view a specific Shelter by ID
    path("/shelters/<int:shelter_id>/", views.ShowShelterPage.as_view(), name="shelter"),
    
    # Route to create a new Shelter
    path("/shelters/create/", views.CreateSheltersPage.as_view(), name="create_shelter"),
    
    # Route to update a specific Shelter by ID
    path("/shelters/<int:shelter_id>/update/", views.UpdateShelterPage.as_view(), name="update_shelter"),
    
    
    # Route to view all Pets
    path("/pets/", views.ShowPetsPage.as_view(), name="pets"),
    
    # Route to view a specific Pet by ID
    path("/pets/<int:pet_id>/", views.ShowPetPage.as_view(), name="pet"),
    
    # Route to create a new Pet
    path("/pets/create/", views.CreatePetsPage.as_view(), name="create_pet"),
    
    # Route to update a specific Pet by ID
    path("/pets/<int:pet_id>/update/", views.UpdatePetPage.as_view(), name="update_pet"),
    
    # Route to delete a specific Pet
    path("/pets/<int:pet_id>/delete/", views.DeletePetPage.as_view(), name="delete_pet"),
    
    
    # Route for Shelters to View all adoptions
    
    path("/adoptions", views.ViewAdoptionPage.as_view(), name="view_adoptions"),
    
    # Route for pet owners to adopt a Pet
    
    path("/adoptions/<int:pet_id>", views.CreateAdoptionPage.as_view(), name="view_adoption"),
    
    # Route for shelters to update status on adoption
    
    path("/adoptions/<int:adoption_id>/update/", views.UpdateAdoptionPage.as_view(), name="update_adoption"),
    
    # Route for shelters to delete adoption
    
    path("/adoptions/<int:adoption_id>/delete/", views.DeleteAdoptionPage.as_view(), name="delete_adoption"),
    
    
    
    # Route for pet owners to view their adoptions
    
    path("/my_adoptions", views.ViewMyAdoptionsPage.as_view(), name="view_my_adoptions"),
    
    # Route for pet owners to view their adoptions
    
    path("/my_adoptions/<int:adoption_id>", views.ViewMyAdoptionPage.as_view(), name="view_my_adoption"),
    
    

    # Route for Users to comment on Pet profile 
    
    path("/comments/create/<int:pet_id>/", views.CreatePetProfilePage.as_view(),name="pet_create_comment"),
    
     # Route for Users to delete comments on Pet profile 
    
    path("/comments/delete/<int:pet_id>", views.DeletePetProfilePage.as_view(), name="pet_delete_comment"),
    
    
    # Route used for filtering pet profiles based on pet name or age/breed
    path("/pets/search/", views.FilterPetPage.as_view(), name="pet_search"),
    
    
    # Route used for filtering shelter profiles based of Shelter name
    path("/shelters/search/", views.FilterShelterPage.as_view(), name="shelter_search"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT), # added for serving media files in production environment.
    
