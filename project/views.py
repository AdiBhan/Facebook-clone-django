from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Q
from .models import Shelter, Pet, AdoptionRequest, Comment, ShelterReview
from .forms import AdoptionRequestForm, CommentForm, ShelterReviewForm, UserRegistrationForm
from django.utils import timezone
from django.contrib.auth import login
class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

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
            # Shelter employees see adoptions for their shelter
            return AdoptionRequest.objects.filter(shelter=self.request.user)

class CreateAdoptionPage(LoginRequiredMixin, CreateView):
    model = AdoptionRequest
    form_class = AdoptionRequestForm
    template_name = 'project/adoption_create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = get_object_or_404(Pet, pk=self.kwargs['pet_id'])
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pet_id'])
        form.instance.shelter = form.instance.pet.shelter
        form.instance.status = 'PENDING'
        form.instance.date_requested = timezone.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('view_my_adoptions')



class DeleteAdoptionRequestView(LoginRequiredMixin, DeleteView):
    model = AdoptionRequest
    template_name = 'project/adoption_delete.html'
    pk_url_kwarg = 'adoption_id'
    success_url = reverse_lazy('view_my_adoptions')

    def dispatch(self, request, *args, **kwargs):
        adoption = self.get_object()
        if not (adoption.user == request.user and adoption.status == 'PENDING'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# Comment Views
class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'project/comment_create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = get_object_or_404(Pet, pk=self.kwargs['pet_id'])
        return context
    
    def form_valid(self, form):
        # Using the authenticated user directly
        form.instance.user = self.request.user
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pet_id'])
        form.instance.date_posted = timezone.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('pet', kwargs={'pk': self.kwargs['pet_id']})

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'project/comment_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('pet', kwargs={'pk': self.object.pet.pk})
class UpdateCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'project/comment_edit.html'
    
    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = self.object.pet
        return context
    
    def get_success_url(self):
        return reverse_lazy('pet', kwargs={'pk': self.object.pet.id})
    
# Search Views
class FilterPetPage(ListView):
    model = Pet
    template_name = 'project/pets_list.html' 
    context_object_name = 'pets'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        pet_type = self.request.GET.get('pet_type', '')
        shelter = self.request.GET.get('shelter', '')
        min_age = self.request.GET.get('min_age')
        max_age = self.request.GET.get('max_age')

        queryset = Pet.objects.all()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(breed__icontains=query) |
                Q(description__icontains=query)
            )
        
        if pet_type:
            queryset = queryset.filter(pet_type=pet_type)
            
        if shelter:
            queryset = queryset.filter(shelter=shelter)
            
        if min_age:
            queryset = queryset.filter(age__gte=min_age)

        if max_age:
            queryset = queryset.filter(age__lte=max_age)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shelters'] = Shelter.objects.all()  # For shelter dropdown
        # Preserve search parameters in pagination
        context['current_type'] = self.request.GET.get('pet_type', '')
        context['current_shelter'] = self.request.GET.get('shelter', '')
        context['current_min_age'] = self.request.GET.get('min_age', '')
        context['current_max_age'] = self.request.GET.get('max_age', '')
        context['current_query'] = self.request.GET.get('q', '')
        return context

class FilterShelterPage(ListView):
    model = Shelter
    template_name = 'project/shelter_list.html'  # Change this to match your template path
    context_object_name = 'shelters'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        min_rating = self.request.GET.get('min_rating')
        
        queryset = Shelter.objects.all()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query) |
                Q(description__icontains=query)
            ) 
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)
            
        return queryset.order_by('-average_rating')  # Sort by rating by default
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_rating'] = self.request.GET.get('min_rating', '')
        context['current_query'] = self.request.GET.get('q', '')
        return context
    

class CreateShelterReviewView(LoginRequiredMixin, CreateView):
    model = ShelterReview
    form_class = ShelterReviewForm
    template_name = 'project/shelter_review_create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shelter'] = get_object_or_404(Shelter, pk=self.kwargs['shelter_id'])
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.shelter = get_object_or_404(Shelter, pk=self.kwargs['shelter_id'])
        form.instance.date_posted = timezone.now()
        response = super().form_valid(form)
        self.update_shelter_rating(form.instance.shelter)
        return response
    
    def get_success_url(self):
        return reverse_lazy('shelter', kwargs={'pk': self.kwargs['shelter_id']})
        
    def update_shelter_rating(self, shelter):
        reviews = ShelterReview.objects.filter(shelter=shelter)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        shelter.average_rating = round(avg_rating) if avg_rating else 0
        shelter.save()
class UpdateShelterReviewView(LoginRequiredMixin, UpdateView):
    model = ShelterReview
    form_class = ShelterReviewForm
    template_name = 'project/shelter_review_edit.html'
    
    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if request.user != review.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shelter'] = self.get_object().shelter
        return context
    
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

class DeleteShelterReviewView(LoginRequiredMixin, DeleteView):
    model = ShelterReview
    template_name = 'project/shelter_review_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if request.user != review.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.get_object()
        context['shelter'] = self.get_object().shelter
        return context
    
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