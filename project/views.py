from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Shelter, Pet, AdoptionRequest, Comment, ShelterReview
from .forms import PetForm, ShelterForm, AdoptionRequestForm, CommentForm, ShelterReviewForm
from django.db.models import Avg

class HomePage(TemplateView):
    template_name = 'project/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_pets'] = Pet.objects.all().order_by('-id')[:6]
        context['top_shelters'] = Shelter.objects.all().order_by('-average_rating')[:3]
        return context

# Shelter Views
class ShowSheltersPage(ListView):
    model = Shelter
    template_name = 'project/shelter_list.html'
    context_object_name = 'shelters'
    paginate_by = 10

class ShowShelterPage(DetailView):
    model = Shelter
    template_name = 'project/shelter_details.html'
    context_object_name = 'shelter'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pets'] = Pet.objects.filter(shelter=self.object)
        context['reviews'] = ShelterReview.objects.filter(shelter=self.object)
        return context

class CreateSheltersPage(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Shelter
    form_class = ShelterForm
    template_name = 'project/shelter_create.html'
    success_url = reverse_lazy('shelters')
    
    def test_func(self):
        return self.request.user.is_shelter_employee

class UpdateShelterPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Shelter
    form_class = ShelterForm
    template_name = 'project/shelter_update.html'
    
    def test_func(self):
        return self.request.user.is_shelter_employee
    
    def get_success_url(self):
        return reverse_lazy('shelter', kwargs={'pk': self.object.pk})

# Pet Views
class ShowPetsPage(ListView):
    model = Pet
    template_name = 'project/pets_list.html'
    context_object_name = 'pets'
    paginate_by = 12

class ShowPetPage(DetailView):
    model = Pet
    template_name = 'project/pets_detail.html'
    context_object_name = 'pet'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(pet=self.object)
        context['adoption_form'] = AdoptionRequestForm()
        return context

class CreatePetsPage(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'project/pets_create.html'
    
    def test_func(self):
        return self.request.user.is_shelter_employee
    
    def form_valid(self, form):
        form.instance.shelter = self.request.user.shelter
        return super().form_valid(form)

class UpdatePetPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'project/pets_update.html'
    
    def test_func(self):
        return self.request.user.is_shelter_employee and self.get_object().shelter == self.request.user.shelter

class DeletePetPage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pet
    template_name = 'project/pets_delete.html'
    success_url = reverse_lazy('pets')
    
    def test_func(self):
        return self.request.user.is_shelter_employee and self.get_object().shelter == self.request.user.shelter

# Adoption Views

class ViewMyAdoptionsPage(LoginRequiredMixin, ListView):
    model = AdoptionRequest
    template_name = 'project/my_adoptions.html'
    context_object_name = 'adoptions'
    
    def get_queryset(self):
        return AdoptionRequest.objects.filter(user=self.request.user)

class ViewMyAdoptionPage(LoginRequiredMixin, DetailView):
    model = AdoptionRequest
    template_name = 'project/adoption_detail.html'
    context_object_name = 'adoption'
    pk_url_kwarg = 'adoption_id'
    
    def get_queryset(self):
        return AdoptionRequest.objects.filter(user=self.request.user)

class ViewAdoptionPage(LoginRequiredMixin, ListView):
    model = AdoptionRequest
    template_name = 'project/adoption_list.html'
    context_object_name = 'adoptions'
    
    def get_queryset(self):
        if self.request.user.is_shelter_employee:
            # Shelter employees see adoptions for their shelter
            return AdoptionRequest.objects.filter(shelter=self.request.user.shelter)
        else:
            # Regular users see their own adoptions
            return AdoptionRequest.objects.filter(user=self.request.user)

class CreateAdoptionPage(LoginRequiredMixin, CreateView):
    model = AdoptionRequest
    form_class = AdoptionRequestForm
    template_name = 'project/adoption_create.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pet_id'])
        form.instance.shelter = form.instance.pet.shelter
        form.instance.status = 'PENDING'
        form.instance.date_requested = timezone.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('view_my_adoptions')
class UpdateAdoptionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AdoptionRequest
    fields = ['status', 'notes']
    template_name = 'project/adoption_update.html'
    pk_url_kwarg = 'adoption_id'
    
    def test_func(self):
        adoption = self.get_object()
        return self.request.user.is_shelter_employee and adoption.shelter == self.request.user.shelter
    
    def form_valid(self, form):
        if form.instance.status == 'APPROVED':
            form.instance.date_approved = timezone.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('view_adoptions')

class DeleteAdoptionPage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AdoptionRequest
    template_name = 'project/adoption_delete.html'
    pk_url_kwarg = 'adoption_id'
    success_url = reverse_lazy('view_adoptions')
    
    def test_func(self):
        adoption = self.get_object()
        return (self.request.user.is_shelter_employee and 
                adoption.shelter == self.request.user.shelter) or \
               (adoption.user == self.request.user and adoption.status == 'PENDING')

# Comment Views
class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'project/comment_create.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pet_id'])
        return super().form_valid(form)

class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'project/comment_delete.html'
    
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
    

class CreateShelterReviewView(LoginRequiredMixin, CreateView):
    model = ShelterReview
    form_class = ShelterReviewForm
    template_name = 'shelters/reviews/create.html'
    
    def form_valid(self, form):
        # Set the user and shelter
        form.instance.user = self.request.user
        form.instance.shelter = get_object_or_404(Shelter, pk=self.kwargs['shelter_id'])
        form.instance.date_posted = timezone.now()
        
        # Update shelter's average rating
        response = super().form_valid(form)
        self.update_shelter_rating(form.instance.shelter)
        return response
    
    def get_success_url(self):
        return reverse_lazy('shelter', kwargs={'pk': self.kwargs['shelter_id']})
    
    def update_shelter_rating(self, shelter):
        # Calculate new average rating
        reviews = ShelterReview.objects.filter(shelter=shelter)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        shelter.average_rating = round(avg_rating) if avg_rating else 0
        shelter.save()

class UpdateShelterReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ShelterReview
    form_class = ShelterReviewForm
    template_name = 'shelters/reviews/update.html'
    
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        self.update_shelter_rating(self.object.shelter)
        return response
    
    def get_success_url(self):
        return reverse_lazy('shelter', kwargs={'pk': self.object.shelter.pk})
    
    def update_shelter_rating(self, shelter):
        reviews = ShelterReview.objects.filter(shelter=shelter)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        shelter.average_rating = round(avg_rating) if avg_rating else 0
        shelter.save()

class DeleteShelterReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ShelterReview
    template_name = 'shelters/reviews/delete.html'
    
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user
    
    def get_success_url(self):
        return reverse_lazy('shelter', kwargs={'pk': self.object.shelter.pk})
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        self.update_shelter_rating(self.object.shelter)
        return response
    
    def update_shelter_rating(self, shelter):
        reviews = ShelterReview.objects.filter(shelter=shelter)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        shelter.average_rating = round(avg_rating) if avg_rating else 0
        shelter.save()