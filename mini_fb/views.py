from django.shortcuts import render
from .models import Profile, StatusMessage
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse, reverse_lazy
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

    
class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})