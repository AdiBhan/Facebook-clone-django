# project/models.py

from django.db import models
from django.contrib.auth import get_user_model

# Get User model
User = get_user_model()

class Shelter(models.Model):
    """
    Animal shelter model. Contains shelter details and links to pets.
    """
    name = models.CharField(max_length=255, unique=True)  # Shelter name
    address = models.CharField(max_length=255)  # Address
    contact_info = models.TextField()  # Contact info
    location = models.CharField(max_length=100)  # City/area
    capacity = models.IntegerField()  # Pet capacity
    description = models.TextField()  # Description
    average_rating = models.IntegerField()  # Rating
    
    def __str__(self):
        """Returns shelter name and location"""
        return f"{self.name} ({self.location})"
    
class Pet(models.Model):
    """
    Pet model. Links to shelter and tracks adoption status.
    """
    PET_TYPES = [
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
        ('OTHER', 'Other'),
    ]
    name = models.CharField(max_length=255)  # Name
    age = models.IntegerField()  # Age
    address = models.CharField(max_length=255)  # Location
    breed = models.CharField(max_length=255)  # Breed
    image_url = models.URLField(max_length=255) # Photos
    shelter = models.ForeignKey(Shelter, blank=True, on_delete=models.CASCADE)  # Shelter
    pet_type = models.TextField(max_length=10, choices=PET_TYPES)  # Type
    description = models.TextField()  # Details
    
    def __str__(self):
        """Returns pet name, type and breed"""
        return f"{self.name} - {self.pet_type} ({self.breed})"
    

class Comment(models.Model):
    """
    Comments on pet profiles by users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Author
    pet = models.ForeignKey(Pet, blank=True, null=True, default=None, on_delete=models.CASCADE)  # Pet
    content = models.TextField()  # Content
    date_posted = models.DateTimeField()  # Date
    
    def __str__(self):
        """Returns comment author and pet"""
        return f"Comment by {self.user} on {self.pet}"
    
class ShelterReview(models.Model):
    """
    User reviews of shelters with ratings.
    """
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)  # Reviewer
    shelter = models.ForeignKey(Shelter, blank=True, null=True, on_delete=models.CASCADE)  # Shelter
    rating = models.IntegerField()  # Rating
    review_text = models.TextField()  # Review
    date_posted = models.DateTimeField()  # Date
    
    def __str__(self):
        """Returns shelter review info with rating"""
        return f"Review of {self.shelter} by {self.user} - {self.rating}/5"
    
class AdoptionRequest(models.Model):
    """
    Adoption request linking user, pet and shelter.
    """
    pet = models.ForeignKey(Pet, blank=True, null=True, on_delete=models.CASCADE)  # Pet
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)  # User
    shelter = models.ForeignKey(Shelter, blank=True, null=True, on_delete=models.CASCADE)  # Shelter
    status = models.TextField()  # Status
    date_requested = models.DateTimeField()  # Request date
    date_approved = models.DateTimeField(null=True)  # Approval date
    notes = models.TextField()  # Notes
    
    def __str__(self):
        """Returns adoption request summary"""
        return f"Adoption request for {self.pet} by {self.user} - {self.status}"