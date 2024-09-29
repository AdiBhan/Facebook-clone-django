from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import time
import random

# Create your views here.



# Restaurant Data
menu:object = {
            'hotdog': 2.99,
            'burger': 4.99,
            'lobster': 11.49,
            'steak': 9.99,
            'soda': 1.49,
            # Special Daily Items
            'Lobster': 11.49,
            'Chicken': 9.99,
            'BBQ': 14.99,
            'Grilled': 13.99,
           
        }

def main(request: HttpRequest) -> HttpResponse:
    ''' Function to return the home page of the restaurant app. '''
    
    
    return render(request, 'restaurant/main.html')



def order(request: HttpRequest) -> HttpResponse:
    ''' Function to render the order page of the restaurant app. '''
    
    ## List of daily specials items for the current day. We will select a random item from this list each time page is rendered
    daily_specials_items:list = [
    {'name': 'Lobster Bisque', 'price': 11.49, 'description': 'Rich and creamy lobster bisque.'},
    {'name': 'Chicken Alfredo', 'price': 9.99, 'description': 'Grilled chicken with creamy alfredo sauce.'},
    {'name': 'BBQ Ribs', 'price': 14.99, 'description': 'Slow-cooked ribs with BBQ sauce.'},
    {'name': 'Grilled Salmon', 'price': 13.99, 'description': 'Fresh salmon grilled to perfection.'}
]
    
    # Select a random daily special item from the list and render the order page with the selected item
    return render(request, 'restaurant/order.html', context=random.choice(daily_specials_items))


def confirmation(request: HttpRequest) -> HttpResponse:
    ''' Function to render the confirmation page of the restaurant app. '''
    
    
    ## If incoming request method is POST, process the form data and render the confirmation page. Otherwise, redirect back to the order page.
    if request.method == 'POST':
        # Retrieve form data
        name, email,special_instructions = request.POST.get('name'), request.POST.get('email'), request.POST.get('special_instructions', '')
    
        # Initialize variables to store the ordered items and the total price
        ordered_items = []
        total_price = 0

      
       
        print(request.POST)
        # Update the ordered items and total price based on the form data
        for item, price in menu.items():
            if request.POST.get(item):
                ordered_items.append({'name': item.capitalize(), 'price': price})
                total_price += price

        # Calculate the ready time: pick a random interval between 30 and 60 minutes 
        rand_interval = random.randint(30 * 60, 60 * 60)
        # Get the current time in seconds
        cur_time = time.time()
        # Calculate the ready time by adding the random interval to the current time and format it as a time string
        ready_time = time.strftime('%I:%M %p', time.localtime(cur_time + rand_interval))

        # Render the confirmation page with the provided data
        context = {
            'name': name,
            'email': email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'total_price': total_price,
            'ready_time': ready_time
        }
        return render(request, 'restaurant/confirmation.html', context=context)

    return HttpResponseRedirect('order')
