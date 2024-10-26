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
        # Returns URL for viewing this profile
        return reverse('show_profile', args=[str(self.id)])
    
    
    def get_friends(self):
        ''' Searches all friends tables and returns all friends'''
        friend_1_relations = Friend.objects.filter(friend_1=self).values_list('friend_2', flat=True)
        friend_2_relations = Friend.objects.filter(friend_2=self).values_list('friend_1', flat=True)

        
        friend_ids = list(friend_1_relations) + list(friend_2_relations)
        
        return Profile.objects.filter(id__in=friend_ids)
    def get_friend_suggestions(self):
        current_friends = self.get_friends()
        
        # Friends which aren't yourself or any of your current friends 
        suggestions = Profile.objects.exclude(id=self.id).exclude(id__in=current_friends)

        return suggestions

    def add_friend(self, other):
        ''' Adds friendship between two profiles. '''
        existing_friendship = False
        if self != other:
            existing_friendship = Friend.objects.filter(
                models.Q(friend_1=self, friend_2=other) | models.Q(friend_1=other, friend_2=self)
            ).exists()

        # Only create if no existing friendship is found
        if not existing_friendship:
            Friend.objects.create(friend_1=self, friend_2=other)
            
            
    def get_news_feed(self):
        ''' Returns news feed by combining own statuses and statuses of friends. '''
      
        own_statuses = self.get_status_messages()
        friends = self.get_friends()
        
        friends_statuses = StatusMessage.objects.filter(profile__in=friends)

        news_feed = own_statuses | friends_statuses
        return news_feed.order_by('-timestamp')

class StatusMessage(models.Model):
    # Status model for mini_fb. Contains a message, timestamp of the message and foreign key relationship to Profile
    message = models.CharField(max_length=300)
    timestamp = models.DateTimeField(default=timezone.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        ''' Replaces built-in two string method with custom one that returns first, last name and message. '''
        return f"{self.profile.first_name} {self.profile.last_name}: {self.message[:50]}..."
    
    def get_images(self):
        # Returns a list of images
        return self.image_set.all()

class Image(models.Model):
    # Image model for mini_fb. Contains a timestamp, image file, and a foreign key relationship to StatusMessage.
    
    timestamp = models.DateTimeField(default=timezone.now)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images') 
    image_file = models.ImageField(upload_to='imgs/')  # No related_name needed here

    
class Friend(models.Model):
    # Friend model for mini_fb. Contains two foreign key relationships to Profile, and a timestamp.
    friend_1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    friend_2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.friend_1.first_name} {self.friend_1.last_name} & {self.friend_2.first_name} {self.friend_2.last_name}"