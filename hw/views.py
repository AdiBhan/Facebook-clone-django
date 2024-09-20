# hw/views.py
# description: logic to handle URL requests

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# Create your views here.


# def home(request):
#     ''' Function to respond to the /hw URL'''

#     response_text = f"""
# <html>
#     <h1>Hello World</h1>
#     <p>This is our first Django web page</p>
#     <hr>
#     <p>This page was generated at {time.ctime()}</p>
# </html>
# """

#     return HttpResponse(response_text)


def home(request):
    ''' Function to respond to the /hw URL'''

    template_name = "hw/home.html"

    context = {'current_time': time.ctime(
    ), 'letter1': chr(random.randint(65, 90)), 'letter2': chr(random.randint(65, 90)), 'number': chr(random.randint(1, 10))}

    # delegate response to the template:
    return render(request, template_name, context)


def about(request):
    ''' Function to respond to the /hw/about URL'''

    template_name = "hw/about.html"

    context = {'current_time': time.ctime(
    )}

    # delegate response to the template:
    return render(request, template_name, context)
