# project/views.py


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Q, Count
from .models import Shelter, Pet, AdoptionRequest, Comment, ShelterReview
from .forms import AdoptionRequestForm, CommentForm, ShelterReviewForm, UserRegistrationForm
from django.utils import timezone
from django.contrib.auth import login
from django.db.models import Avg, Count,Max, Min
from django.db import models
class RegisterView(CreateView):
    ''' RegisterView class uses CreateView to render register page and handle user submission redirecting them to the default homepage afterwards
    and checking logging with form_valid() helper method'''
    
    template_name = 'registration/register.html' # template page which will be rendered
    form_class = UserRegistrationForm # Uses UserRegistrationForm form to render form in forms.py file
    success_url = '/' # If registration is successful (user filled out all input fields and no duplicate emails), will redirect to "/"

    def form_valid(self, form):
        ''' form_valid() method saves form and logs user in. Afterward redirects them to index homepage'''
        user = form.save() # saves form
        login(self.request, user)  # logs user in
        return redirect('index') # redirects user to /index page if registration is successful (form is valid)

class HomePage(TemplateView):
    '''HomePage class uses TemplateView to render the index page with recent pets and top-rated shelters'''
    template_name = 'project/index.html'  # template page which will be rendered
    
    def get_context_data(self, **kwargs):
        '''get_context_data method adds recent pets and top shelters to the template context'''
        context = super().get_context_data(**kwargs)
        context['recent_pets'] = Pet.objects.all().order_by('-id')[:6]  # gets 6 most recent pets
        context['top_shelters'] = Shelter.objects.all().order_by('-average_rating')[:3]  # gets top 3 rated shelters
        return context

class ShowSheltersPage(ListView):
    '''ShowSheltersPage class uses ListView to display all shelters with pagination'''
    model = Shelter  # uses Shelter model
    template_name = 'project/shelter_list.html'  # template page which will be rendered
    context_object_name = 'shelters'  # name used to access shelters in template
    paginate_by = 10  # number of shelters per page

class ShowShelterPage(DetailView):
    '''ShowShelterPage class uses DetailView to display detailed information about a specific shelter'''
    model = Shelter  # uses Shelter model
    template_name = 'project/shelter_details.html'  # template page which will be rendered
    context_object_name = 'shelter'  # name used to access shelter in template
    
    def get_context_data(self, **kwargs):
        '''get_context_data method adds shelter's pets and reviews to the template context'''
        context = super().get_context_data(**kwargs)
        context['pets'] = Pet.objects.filter(shelter=self.object)  # gets all pets for this shelter
        context['reviews'] = ShelterReview.objects.filter(shelter=self.object)  # gets all reviews for this shelter
        return context

class ShowPetsPage(ListView):
    '''ShowPetsPage class uses ListView to display all pets with pagination'''
    model = Pet  # uses Pet model
    template_name = 'project/pets_list.html'  # template page which will be rendered
    context_object_name = 'pets'  # name used to access pets in template
    paginate_by = 12  # number of pets per page

class ShowPetPage(DetailView):
    '''ShowPetPage class uses DetailView to display detailed information about a specific pet'''
    model = Pet  # uses Pet model
    template_name = 'project/pets_detail.html'  # template page which will be rendered
    context_object_name = 'pet'  # name used to access pet in template
    
    def get_context_data(self, **kwargs):
        '''get_context_data method adds pet's comments and adoption form to the template context'''
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(pet=self.object)  # gets all comments for this pet
        context['adoption_form'] = AdoptionRequestForm()  # creates new adoption request form
        return context

class ViewMyAdoptionsPage(LoginRequiredMixin, ListView):
    '''ViewMyAdoptionsPage class uses ListView to display all adoption requests for the logged-in user
    LoginRequiredMixin ensures only authenticated users can access this view'''
    model = AdoptionRequest  # uses AdoptionRequest model
    template_name = 'project/my_adoptions.html'  # template page which will be rendered
    context_object_name = 'adoptions'  # name used to access adoptions in template
    
    def get_queryset(self):
        '''get_queryset method filters adoption requests to show only those belonging to the current user'''
        return AdoptionRequest.objects.filter(user=self.request.user)

# Adoption Views
class ViewMyAdoptionsPage(LoginRequiredMixin, ListView):
    '''ViewMyAdoptionsPage class uses ListView to display all adoption requests for the logged-in user.
    LoginRequiredMixin ensures only authenticated users can access this view'''
    model = AdoptionRequest  # uses AdoptionRequest model
    template_name = 'project/my_adoptions.html'  # template page which will be rendered
    context_object_name = 'adoptions'  # name used to access adoptions in template
    
    def get_queryset(self):
        '''get_queryset method filters adoption requests to show only those belonging to the current user'''
        return AdoptionRequest.objects.filter(user=self.request.user)

class ViewMyAdoptionPage(LoginRequiredMixin, DetailView):
    '''ViewMyAdoptionPage class uses DetailView to show detailed information about a specific adoption request.
    LoginRequiredMixin ensures only authenticated users can access this view'''
    model = AdoptionRequest  # uses AdoptionRequest model
    template_name = 'project/adoption_detail.html'  # template page which will be rendered
    context_object_name = 'adoption'  # name used to access adoption in template
    pk_url_kwarg = 'adoption_id'  # URL parameter name for the adoption ID
    
    def get_queryset(self):
        '''get_queryset method ensures users can only view their own adoption requests'''
        return AdoptionRequest.objects.filter(user=self.request.user)


class CreateAdoptionPage(LoginRequiredMixin, CreateView):
    '''CreateAdoptionPage class uses CreateView to handle new adoption request submissions.
    LoginRequiredMixin ensures only authenticated users can create adoption requests'''
    model = AdoptionRequest  # uses AdoptionRequest model
    form_class = AdoptionRequestForm  # form class to handle adoption request creation
    template_name = 'project/adoption_create.html'  # template page which will be rendered
    
    def get_context_data(self, **kwargs):
        '''get_context_data method adds the pet being adopted to the template context'''
        context = super().get_context_data(**kwargs)
        context['pet'] = get_object_or_404(Pet, pk=self.kwargs['pet_id'])  # gets pet by ID or returns 404
        return context # return updated context object
    
    def form_valid(self, form):
        '''form_valid method populates additional fields before saving the adoption request'''
        form.instance.user = self.request.user  # sets the requesting user
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pet_id'])  # sets the pet being requested
        form.instance.shelter = form.instance.pet.shelter  # sets the shelter from the pet
        form.instance.status = 'PENDING'  # sets initial status
        form.instance.date_requested = timezone.now()  # sets request timestamp
        return super().form_valid(form)
    
    def get_success_url(self):
        '''get_success_url method redirects to user's adoption list after successful submission'''
        return reverse_lazy('view_my_adoptions')

class DeleteAdoptionRequestView(LoginRequiredMixin, DeleteView):
    '''DeleteAdoptionRequestView class uses DeleteView to handle deletion of pending adoption requests.
    LoginRequiredMixin ensures only authenticated users can delete requests'''
    model = AdoptionRequest  # uses AdoptionRequest model
    template_name = 'project/adoption_delete.html'  # template page which will be rendered
    pk_url_kwarg = 'adoption_id'  # URL parameter name for the adoption ID
    success_url = reverse_lazy('view_my_adoptions')  # redirect URL after successful deletion

    def dispatch(self, request, *args, **kwargs):
        '''dispatch method ensures only the request creator can delete pending requests'''
        adoption = self.get_object()
        if not (adoption.user == request.user and adoption.status == 'PENDING'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

# Comment Views
class CreateCommentView(LoginRequiredMixin, CreateView):
    '''CreateCommentView class uses CreateView to handle new comment submissions on pets.
    LoginRequiredMixin ensures only authenticated users can create comments'''
    model = Comment  # uses Comment model
    form_class = CommentForm  # form class to handle comment creation
    template_name = 'project/comment_create.html'  # template page which will be rendered
    
    def get_context_data(self, **kwargs):
        '''get_context_data method adds the pet being commented on to the template context'''
        context = super().get_context_data(**kwargs)
        context['pet'] = get_object_or_404(Pet, pk=self.kwargs['pet_id'])  # gets pet by ID or returns 404
        return context
    
    def form_valid(self, form):
        '''form_valid method sets the comment author and pet before saving'''
        form.instance.user = self.request.user  # sets the commenting user
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pet_id'])  # sets the pet being commented on
        form.instance.date_posted = timezone.now()  # sets comment timestamp
        return super().form_valid(form)
    
    def get_success_url(self):
        '''get_success_url method redirects to pet detail page after successful comment'''
        return reverse_lazy('pet', kwargs={'pk': self.kwargs['pet_id']})

# Comment Views
class CreateCommentView(LoginRequiredMixin, CreateView):
    '''CreateCommentView class uses CreateView to handle new comment submissions on pets.
    LoginRequiredMixin ensures only authenticated users can create comments'''
    model = Comment  # uses Comment model
    form_class = CommentForm  # form class to handle comment creation
    template_name = 'project/comment_create.html'  # template page which will be rendered
    
    def get_context_data(self, **kwargs):
        '''get_context_data method adds the pet being commented on to the template context'''
        context = super().get_context_data(**kwargs)
        context['pet'] = get_object_or_404(Pet, pk=self.kwargs['pet_id'])  # gets pet by ID or returns 404
        return context
    
    def form_valid(self, form):
        '''form_valid method sets the comment author and pet before saving'''
        form.instance.user = self.request.user  # sets the commenting user
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pet_id'])  # sets the pet being commented on
        form.instance.date_posted = timezone.now()  # sets comment timestamp
        return super().form_valid(form)
    
    def get_success_url(self):
        '''get_success_url method redirects to pet detail page after successful comment'''
        return reverse_lazy('pet', kwargs={'pk': self.kwargs['pet_id']})
class DeleteCommentView(LoginRequiredMixin, DeleteView):
    '''DeleteCommentView class uses DeleteView to handle deletion of comments.
    LoginRequiredMixin ensures only authenticated users can delete comments'''
    model = Comment  # uses Comment model
    template_name = 'project/comment_delete.html'  # template page which will be rendered
    
    def dispatch(self, request, *args, **kwargs):
        '''dispatch method ensures only the comment author can delete the comment'''
        comment = self.get_object()
        if request.user != comment.user: # if user isn't the author (the foreign key of the comment and user don't match)
            raise PermissionDenied # return permission denied
        return super().dispatch(request, *args, **kwargs) # otherwise successful
    
    def get_success_url(self):
        '''get_success_url method redirects to pet detail page after successful deletion'''
        return reverse_lazy('pet', kwargs={'pk': self.object.pet.pk})

class UpdateCommentView(LoginRequiredMixin, UpdateView):
    '''UpdateCommentView class uses UpdateView to handle editing of existing comments.
    LoginRequiredMixin ensures only authenticated users can edit comments'''
    model = Comment  # uses Comment model
    form_class = CommentForm  # form class to handle comment editing
    template_name = 'project/comment_edit.html'  # template page which will be rendered
    
    def dispatch(self, request, *args, **kwargs):
        '''dispatch method ensures only the comment author can edit the comment'''
        comment = self.get_object()
        if request.user != comment.user: ##  if user isn't the author (the foreign key of the comment and user don't match)
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''get_context_data method adds the pet being commented on to the template context'''
        context = super().get_context_data(**kwargs)
        context['pet'] = self.object.pet  # adds pet to context
        return context # return updated coontext object
    
    def get_success_url(self):
        '''get_success_url method redirects to pet detail page after successful edit'''
        return reverse_lazy('pet', kwargs={'pk': self.object.pet.id})
    
# Search Views
class FilterPetPage(ListView):
    '''FilterPetPage class uses ListView to display filtered pet results based on search criteria'''
    model = Pet  # uses Pet model
    template_name = 'project/pets_list.html'  # template page which will be rendered
    context_object_name = 'pets'  # name used to access pets in template
    paginate_by = 12  # number of pets per page
    
    def get_queryset(self):
        '''get_queryset method filters pets based on search parameters: name, type, shelter, and age range'''
        query = self.request.GET.get('q', '')  # gets search query parameter
        pet_type = self.request.GET.get('pet_type', '')  # gets pet type filter
        shelter = self.request.GET.get('shelter', '')  # gets shelter filter
        min_age = self.request.GET.get('min_age')  # gets minimum age filter
        max_age = self.request.GET.get('max_age')  # gets maximum age filter
        
        queryset = Pet.objects.all()  # starts with all pets
        
        # Applies text search filter based on name, breed and description
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(breed__icontains=query) |
                Q(description__icontains=query)
            )
        
        # If pet type exists, we filter by pet_type
        if pet_type:
            queryset = queryset.filter(pet_type=pet_type)
            
        # If shelter exists, we filter by shelter
        if shelter:
            queryset = queryset.filter(shelter=shelter)
            
        # If min_age or max_age exists, we filter by age range.
        if min_age:
            queryset = queryset.filter(age__gte=min_age)
        if max_age:
            queryset = queryset.filter(age__lte=max_age)

        return queryset # return any filtered data found

    def get_context_data(self, **kwargs):
        '''get_context_data() method preserves search parameters in context for pagination and form pre-filling'''
        context = super().get_context_data(**kwargs)
        context['shelters'] = Shelter.objects.all()  # adds all shelters for dropdown
        # Preserves search parameters
        context['current_type'] = self.request.GET.get('pet_type', '') # check if 'pet_type' exists in current record and save it to current_type variable in context, else save as empty string
        context['current_shelter'] = self.request.GET.get('shelter', '')  # check if 'shelter' exists in current record and save it to current_shelter variable in context, else save as empty string
        context['current_min_age'] = self.request.GET.get('min_age', '') # check if 'min_age' exists in current record and save it to current_min_age variable in context, else save as empty string
        context['current_max_age'] = self.request.GET.get('max_age', '')  # check if 'max_age' exists in current record and save it to current_max_age variable in context, else save as empty string
        context['current_query'] = self.request.GET.get('q', '')  # check if 'q' exists in current record and save it to current_query variable in context, else savve as empty string
        return context # save updated context object

class FilterShelterPage(ListView):
    '''FilterShelterPage class uses ListView to display filtered shelter results based on search criteria'''
    model = Shelter  # uses Shelter model
    template_name = 'project/shelter_list.html'  # template page which will be rendered
    context_object_name = 'shelters'  # name used to access shelters in template
    paginate_by = 12  # number of shelters per page
    
    def get_queryset(self):
        '''get_queryset method filters shelters based on search query and minimum rating'''
        query = self.request.GET.get('q', '')  # gets search query parameter
        min_rating = self.request.GET.get('min_rating')  # gets minimum rating filter
        
        queryset = Shelter.objects.all()  # starts with all shelters

         
        # Applies text search filter based on name, location  and description
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query) |
                Q(description__icontains=query)
            ) 
        # If min rating is found, we filter queryset by min rating
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)
            
        return queryset.order_by('-average_rating')  # return filtered data in descending order by average rating
    
    def get_context_data(self, **kwargs):
        '''get_context_data method preserves search parameters in context for pagination and form pre-filling'''
        context = super().get_context_data(**kwargs)
        context['current_rating'] = self.request.GET.get('min_rating', '')
        context['current_query'] = self.request.GET.get('q', '')
        return context # save updated context object

class CreateShelterReviewView(LoginRequiredMixin, CreateView):
    '''CreateShelterReviewView class uses CreateView to handle new shelter review submissions.
    LoginRequiredMixin ensures only authenticated users can create reviews'''
    model = ShelterReview  # uses ShelterReview model
    form_class = ShelterReviewForm  # form class to handle review creation
    template_name = 'project/shelter_review_create.html'  # template page which will be rendered
    
    def get_context_data(self, **kwargs):
        '''get_context_data method adds the shelter being reviewed to the template context'''
        context = super().get_context_data(**kwargs)
        context['shelter'] = get_object_or_404(Shelter, pk=self.kwargs['shelter_id'])
        return context # save updated context object
    
    def form_valid(self, form):
        '''form_valid method sets review author and shelter, updates shelter rating after saving'''
        form.instance.user = self.request.user  # sets the reviewing user
        form.instance.shelter = get_object_or_404(Shelter, pk=self.kwargs['shelter_id'])  # sets the shelter
        form.instance.date_posted = timezone.now()  # sets review timestamp
        response = super().form_valid(form)
        self.update_shelter_rating(form.instance.shelter)  # updates shelter's average rating
        return response
    
    def get_success_url(self):
        '''get_success_url method redirects to shelter detail page after successful review'''
        return reverse_lazy('shelter', kwargs={'pk': self.kwargs['shelter_id']})
        
    def update_shelter_rating(self, shelter):
        '''update_shelter_rating method recalculates and updates shelter's average rating'''
        reviews = ShelterReview.objects.filter(shelter=shelter)  # gets all reviews for shelter
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']  # calculates average rating
        shelter.average_rating = round(avg_rating) if avg_rating else 0  # updates shelter's rating
        shelter.save() # save shelter row 

class UpdateShelterReviewView(LoginRequiredMixin, UpdateView):
    '''UpdateShelterReviewView class uses UpdateView to handle editing of existing shelter reviews.
    LoginRequiredMixin ensures only authenticated users can edit reviews'''
    model = ShelterReview  # uses ShelterReview model
    form_class = ShelterReviewForm  # form class to handle review editing
    template_name = 'project/shelter_review_edit.html'  # template page which will be rendered
    
    def dispatch(self, request, *args, **kwargs):
        '''dispatch method ensures only the review author can edit the review'''
        review = self.get_object()
        if request.user != review.user: # if user isn't the review author (foreign key of review author isn't same as user) return Permission Denied
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs) # else they have permission
    
    def get_context_data(self, **kwargs):
        '''get_context_data method adds the shelter being reviewed to the template context'''
        context = super().get_context_data(**kwargs)
        context['shelter'] = self.get_object().shelter # Add 'shelter' variable to context to be accessed in template
        return context # return context object
    
    def form_valid(self, form):
        '''form_valid method updates shelter rating after saving edited review'''
        response = super().form_valid(form)
        self.update_shelter_rating(self.object.shelter) # call update_shelter_rating() helper function to update rating
        return response
    
    def get_success_url(self):
        '''get_success_url method redirects to shelter detail page after successful edit'''
        return reverse_lazy('shelter', kwargs={'pk': self.object.shelter.pk})
    
    def update_shelter_rating(self, shelter):
        '''update_shelter_rating method recalculates and updates shelter's average rating'''
        reviews = ShelterReview.objects.filter(shelter=shelter)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] # calculate aggregate of average ratings
        shelter.average_rating = round(avg_rating) if avg_rating else 0 # round rating to nearest whole number so it can fit in 1-5
        shelter.save()

class DeleteShelterReviewView(LoginRequiredMixin, DeleteView):
    '''DeleteShelterReviewView class uses DeleteView to handle deletion of shelter reviews.
    LoginRequiredMixin ensures only authenticated users can delete reviews'''
    model = ShelterReview  # uses ShelterReview model
    template_name = 'project/shelter_review_delete.html'  # template page which will be rendered
    
    def dispatch(self, request, *args, **kwargs):
        '''dispatch method ensures only the review author can delete the review'''
        review = self.get_object()
        if request.user != review.user:  # if user isn't the review author (foreign key of review author isn't same as user) return Permission Denied
            raise PermissionDenied  # return permission denied
        return super().dispatch(request, *args, **kwargs) # else return, they have permission
    
    def get_context_data(self, **kwargs):
        '''get_context_data method adds review and shelter information to the template context'''
        context = super().get_context_data(**kwargs)
        context['review'] = self.get_object() # add 'review' variable to context to access in shelter_review_delete template
        context['shelter'] = self.get_object().shelter  # add 'shelter' variable to context to access in shelter_review_delete template
        return context # return context object
    
    def get_success_url(self):
        '''get_success_url method redirects to shelter detail page after successful deletion'''
        return reverse_lazy('shelter', kwargs={'pk': self.object.shelter.pk})
    
    def delete(self, request, *args, **kwargs):
        '''delete method updates shelter rating after deleting review'''
        response = super().delete(request, *args, **kwargs)
        self.update_shelter_rating(self.object.shelter)  # call update_shelter_rating() helper function to update rating
        return response
    
    def update_shelter_rating(self, shelter):
        '''update_shelter_rating method recalculates and updates shelter's average rating'''
        reviews = ShelterReview.objects.filter(shelter=shelter)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']  # calculate aggregate of average ratings
        shelter.average_rating = round(avg_rating) if avg_rating else 0 # round rating to nearest whole number so it can fit in 1-5
        shelter.save() # save shelter data
        
class ShelterReportView(TemplateView):
    '''ShelterReportView class uses TemplateView to generate comprehensive analytics report about shelter performance.
    Provides detailed statistics about shelters, pets, adoptions, and system metrics'''
    template_name = 'project/shelters_report.html'  # template page which will be rendered

    def get_context_data(self, **kwargs):
        '''get_context_data method aggregates various statistics and metrics for the report.
        Calculates shelter ratings, pet statistics, adoption metrics, and capacity utilization'''
        context = super().get_context_data(**kwargs)

        # Overall shelter statistics
        total_shelters = Shelter.objects.count()  # gets total number of shelters
        avg_shelter_rating = ShelterReview.objects.aggregate(Avg('rating'))['rating__avg']  # calculates average rating across all shelters
        max_shelter_rating = ShelterReview.objects.aggregate(Max('rating'))['rating__max']  # finds highest shelter rating
        min_shelter_rating = ShelterReview.objects.aggregate(Min('rating'))['rating__min']  # finds lowest shelter rating

        # Add shelter statistics to context
        context.update({
            'total_shelters': total_shelters,
            'avg_shelter_rating': avg_shelter_rating,
            'max_shelter_rating': max_shelter_rating,
            'min_shelter_rating': min_shelter_rating,
        })

        # Pet statistics
        total_pets = Pet.objects.count()  # gets total number of pets in system
        pets_by_type = Pet.objects.values('pet_type').annotate(count=Count('id')).order_by('-count')  # counts pets by type, ordered by most common
        most_popular_pet_type = pets_by_type[0] if pets_by_type else None  # identifies most common pet type

        # Add pet statistics to context
        context.update({
            'total_pets': total_pets,
            'pets_by_type': pets_by_type,
            'most_popular_pet_type': most_popular_pet_type,
        })

        # Adoption statistics
        adoption_requests = AdoptionRequest.objects.all()  # gets all adoption requests
        total_adoption_requests = adoption_requests.count()  # counts total requests
        pending_requests = adoption_requests.filter(status='PENDING').count()  # counts pending requests
        approved_requests = adoption_requests.filter(status='APPROVED').count()  # counts approved requests
        # Calculates percentage of requests that are pending
        pending_percentage = (pending_requests / total_adoption_requests * 100) if total_adoption_requests else 0

        # Add adoption statistics to context
        context.update({
            'total_adoption_requests': total_adoption_requests,
            'pending_requests': pending_requests,
            'approved_requests': approved_requests,
            'pending_percentage': pending_percentage,
        })

        # Available pets calculation
        pets_with_approved_adoptions = AdoptionRequest.objects.filter(
            status='APPROVED').values_list('pet_id', flat=True)  # gets IDs of pets with approved adoptions
        available_pets = Pet.objects.exclude(id__in=pets_with_approved_adoptions).count()  # counts pets without approved adoptions

        context['available_pets'] = available_pets

        # Shelter occupancy calculations
        shelters = Shelter.objects.annotate(
            current_occupancy=Count('pet'),  # counts current number of pets in each shelter
            capacity_utilization=100 * Count('pet') / models.F('capacity')  # calculates percentage of capacity used
        ).filter(capacity__gt=0).order_by('-capacity_utilization')  # filters out zero-capacity shelters, orders by utilization

        context['shelter_occupancy'] = shelters

        return context  # returns complete context with all statistics
    
    