from django.db import models

# Create your models here.

class Profile(models.Model):
    # Profile model for mini_fb. Contains: first_name, last_name, city , email_address & profile_image_url
    first_name = models.CharField(max_length=30)  
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email_address = models.EmailField()
    profile_image_url = models.URLField(max_length=200) 
    
    
    # Defined special print method for debugging purposes (when I created records)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"