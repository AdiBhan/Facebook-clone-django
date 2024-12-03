from django.db import models

class Shelter(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    contact_info = models.TextField()
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    description = models.TextField()
    average_rating = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} ({self.location})"
    
class Pet(models.Model):
    PET_TYPES = [
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
        ('OTHER', 'Other'),
    ]
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    image = models.ImageField(max_length=255, upload_to='pet_images/')
    shelter = models.ForeignKey(Shelter, blank=True, on_delete=models.CASCADE)
    pet_type = models.TextField(max_length=10, choices=PET_TYPES)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.name} - {self.pet_type} ({self.breed})"
    
class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    join_date = models.DateField(null=True)
    is_shelter_employee = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
class Comment(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, blank=True, null=True, default=None, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField()
    
    def __str__(self):
        return f"Comment by {self.user} on {self.pet}"
    
class ShelterReview(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    shelter = models.ForeignKey(Shelter, blank=True, null=True, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    date_posted = models.DateTimeField()
    
    def __str__(self):
        return f"Review of {self.shelter} by {self.user} - {self.rating}/5"
    
class AdoptionRequest(models.Model):
    pet = models.ForeignKey(Pet, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    shelter = models.ForeignKey(Shelter, blank=True, null=True, on_delete=models.CASCADE)
    status = models.TextField()
    date_requested = models.DateTimeField()
    date_approved = models.DateTimeField(null=True)
    notes = models.TextField()
    
    def __str__(self):
        return f"Adoption request for {self.pet} by {self.user} - {self.status}"
    
class PetStory(models.Model):
    pet = models.ForeignKey(Pet, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    story = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.pet}"