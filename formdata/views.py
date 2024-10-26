from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.


def show_form(request):
    '''Show the HTML form to the client.'''
    
    # use this templare to produce the response
    template_name= 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    '''Handle the form submission. Read out the data and generate the response.'''
    
    template_name = 'formdata/confirmation.html'
    
    # read out the data from the form data into pyton variables
    
    if request.POST:
        
        # read out the data from the form data into pyton variables
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']
        
        # create a dictionary for the context
        context = {
            'name': name,
            'favorite_color': favorite_color
        }
    
    ## If the client got here by making a get on this URL, send back the form
    template_name= 'formdata/form.html'
    return render(request, template_name,context)

