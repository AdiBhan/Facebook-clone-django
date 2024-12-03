from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Shelter, Pet, AdoptionRequest, Comment, ShelterReview
from .forms import PetForm, ShelterForm, AdoptionRequestForm, CommentForm, ShelterReviewForm

class HomePage(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_pets'] = Pet.objects.all().order_by('-id')[:6]
        context['top_shelters'] = Shelter.objects.all().order_by('-average_rating')[:3]
        return context

# Shelter Views
class ShowSheltersPage(ListView):
    model = Shelter
    template_name = 'shelters/list.html'
    context_object_name = 'shelters'
    paginate_by = 12

class ShowShelterPage(DetailView):
    model = Shelter
    template_name = 'shelters/detail.html'
    context_object_name = 'shelter'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pets'] = Pet.objects.filter(shelter=self.object)
        context['reviews'] = ShelterReview.objects.filter(shelter=self.object)
        return context

class CreateSheltersPage(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Shelter
    form_class = ShelterForm
    template_name = 'shelters/create.html'
    success_url = reverse_lazy('shelters')
    
    def test_func(self):
        return self.request.user.is_shelter_employee

class UpdateShelterPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Shelter
    form_class = ShelterForm
    template_name = 'shelters/update.html'
    
    def test_func(self):
        return self.request.user.is_shelter_employee
    
    def get_success_url(self):
        return reverse_lazy('shelter', kwargs={'pk': self.object.pk})

# Pet Views
class ShowPetsPage(ListView):
    model = Pet
    template_name = 'pets/list.html'
    context_object_name = 'pets'
    paginate_by = 12

class ShowPetPage(DetailView):
    model = Pet
    template_name = 'pets/detail.html'
    context_object_name = 'pet'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(pet=self.object)
        context['adoption_form'] = AdoptionRequestForm()
        return context

class CreatePetsPage(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/create.html'
    
    def test_func(self):
        return self.request.user.is_shelter_employee
    
    def form_valid(self, form):
        form.instance.shelter = self.request.user.shelter
        return super().form_valid(form)

class UpdatePetPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/update.html'
    
    def test_func(self):
        return self.request.user.is_shelter_employee and self.get_object().shelter == self.request.user.shelter

class DeletePetPage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pet
    template_name = 'pets/delete.html'
    success_url = reverse_lazy('pets')
    
    def test_func(self):
        return self.request.user.is_shelter_employee and self.get_object().shelter == self.request.user.shelter

# Adoption Views
class ViewAdoptionPage(LoginRequiredMixin, ListView):
    model = AdoptionRequest
    template_name = 'adoptions/list.html'
    context_object_name = 'adoptions'
    
    def get_queryset(self):
        if self.request.user.is_shelter_employee:
            return AdoptionRequest.objects.filter(shelter=self.request.user.shelter)
        return AdoptionRequest.objects.filter(user=self.request.user)

class CreateAdoptionPage(LoginRequiredMixin, CreateView):
    model = AdoptionRequest
    form_class = AdoptionRequestForm
    template_name = 'adoptions/create.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pet_id'])
        form.instance.shelter = form.instance.pet.shelter
        form.instance.status = 'PENDING'
        return super().form_valid(form)

# Comment Views
class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/create.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pet_id'])
        return super().form_valid(form)

class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user
    
    def get_success_url(self):
        return reverse_lazy('pet', kwargs={'pk': self.object.pet.pk})

# Search Views
class FilterPetPage(ListView):
    model = Pet
    template_name = 'pets/search.html'
    context_object_name = 'pets'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Pet.objects.filter(
                Q(name__icontains=query) |
                Q(breed__icontains=query) |
                Q(description__icontains=query)
            )
        return Pet.objects.all()

class FilterShelterPage(ListView):
    model = Shelter
    template_name = 'shelters/search.html'
    context_object_name = 'shelters'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Shelter.objects.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query) |
                Q(description__icontains=query)
            )
        return Shelter.objects.all()