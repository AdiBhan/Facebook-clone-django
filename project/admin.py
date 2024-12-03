from django.contrib import admin
from .models import Shelter, Pet, Comment, ShelterReview, AdoptionRequest
# Register your models here.

#  Registering models for PetMate
admin.site.register(Shelter)
admin.site.register(Pet)
admin.site.register(Comment)
admin.site.register(ShelterReview)
admin.site.register(AdoptionRequest)
