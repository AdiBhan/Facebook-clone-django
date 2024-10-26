from django.shortcuts import render
from .models import Profile, StatusMessage, Image
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CreateProfileForm, CreateStatusMessageForm,UpdateProfileForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Profile

class ShowAllProfilesView(ListView):
    ''' a view to show all Profiles from template html file show_all_profiles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    ''' View renders one record (Profile) from Profile model'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object 
        context['status_messages'] = profile.get_status_messages()
        return context
    
class CreateProfileView(CreateView):
    ''' View to create a new Profile '''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    # save the status message to database

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        
        return context

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(pk=self.kwargs['pk'])
        # save the status message to database
        sm = form.save()
        print(f"Saved status message: {sm}")
        # read the file from the form:
        files = self.request.FILES.getlist('files')
        print(f"Files: {files}")
        
        for f in files:
            # Create an Image instance
            img = Image(status_message=sm, image_file=f)  # Associate with the saved StatusMessage
            img.save()  # Save the Image object to the database
            print(f"Saved image: {img}")
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the show_profile page after successful creation
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
class UpdateProfileView(UpdateView):
    ''' View to update an existing Profile '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    
    
    def get_success_url(self):
        # Redirect to the show_profile page after successful update
        return reverse_lazy('show_profile', kwargs={'pk': self.object.pk})
    
    
class DeleteStatusMessageView(DeleteView):
    '''' Class to delete a StatusMessage '''
    model = StatusMessage
    context_object_name = 'status_message'
    template_name = 'mini_fb/delete_status_form.html'
    
    def get_success_url(self):
        # Redirect to the profile page associated with the deleted status message
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    
    


class CreateFriendView(View):
    ''' View to add a friend'''
    def dispatch(self, request, *args, **kwargs):
       
        pk = kwargs.get('pk')
        other_pk = kwargs.get('other_pk')
        
        
        # Check to see if primary key has associated Profile Object. (Friendship)
        profile = get_object_or_404(Profile, pk=pk)
        other_profile = get_object_or_404(Profile, pk=other_pk)
        
        profile.add_friend(other_profile)
        
        # Redirect to the profile page (or any other page you prefer)
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(DetailView):
    '''View to show friend suggestions for a profile'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    
    
class ShowNewsFeedView(DetailView):
    
    ''' View to show news feed'''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        # Gets the context object from the profile
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        return context