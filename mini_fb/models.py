from django.db import models
from django.utils import timezone
from django.urls import reverse
class Profile(models.Model):
    # Profile model for mini_fb. Contains: first_name, last_name, city, email_address & profile_image_url
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email_address = models.EmailField()
    profile_image_url = models.URLField(max_length=200)

    def __str__(self):
        ''' Replaces built-in two string method with custom one that returns first and last name. 
            It's called when you print Profile
        '''
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        ''' Returns status messages in decesending order by timestamp'''
        return self.statusmessage_set.order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', args=[str(self.id)])

class StatusMessage(models.Model):
    # Status model for mini_fb. Contains a message, timestamp of the message and foreign key relationship to Profile
    message = models.CharField(max_length=300)
    timestamp = models.DateTimeField(default=timezone.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        ''' Replaces built-in two string method with custom one that returns first, last name and message. '''
        return f"{self.profile.first_name} {self.profile.last_name}: {self.message[:50]}..."
    