from django.contrib import admin
from .models import Shelter, Pet, User, Comment, ShelterReview, AdoptionRequest
# Register your models here.


admin.site.register(Shelter)
admin.site.register(Pet)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(ShelterReview)
admin.site.register(AdoptionRequest)
