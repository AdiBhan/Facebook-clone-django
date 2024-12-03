from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.contrib.auth.forms import UserCreationForm
# Views that don't require login
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['status_messages'] = profile.get_status_messages()
        return context


class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        # Get the user form from POST data
        user_form = UserCreationForm(self.request.POST)
        
        if user_form.is_valid():
            # Create the user
            user = user_form.save()
           
            
            # Attach user to profile
            # form.instance.user = user
            Profile.objects.create(user=user)
            
            # Save the profile
            # response = super().form_valid(form)
            
            # Log the user in
            login(self.request, user)
            
            return response
        else:
            # If user form is invalid, redisplay both forms
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form)
            )

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

# Views that require login
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    login_url = 'login'  # URL to redirect to if user is not logged in

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        
        sm = form.save()
        files = self.request.FILES.getlist('files')
        
        for f in files:
            img = Image(status_message=sm, image_file=f)
            img.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.pk})
    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    context_object_name = 'status_message'
    template_name = 'mini_fb/delete_status_form.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'
    login_url = 'login'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class CreateFriendView(LoginRequiredMixin, View):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, user=request.user)
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])
        
        self.profile.add_friend(other_profile)
        return redirect('show_profile', pk=self.profile.id)

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    login_url = 'login'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        return context
    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)