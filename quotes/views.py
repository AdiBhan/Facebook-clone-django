from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# Create your views here.


##
images: list[str] = ["https://www.johnlennon.com/wp-content/uploads/2022/05/JL.jpg",
                     "https://cdn.britannica.com/84/160284-050-695B1DE3/James-Cameron-2012.jpg",
                     "https://www.amacad.org/sites/default/files/person/headshots/oprah.jpg"]
quotes: list[str] = ["You may say I'm a dreamer, but I'm not the only one. I hope someday you'll join us. And the world will live as one",
                     "If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success.",
                     "If you look at what you have in life, you'll always have more. If you look at what you don't have in life, you'll never have enough. "]


celebs_bio:list[object] = [
    {
        "name": "John Lennon",
        "bio": "John Lennon was an English singer, songwriter, and peace activist who gained worldwide fame as a co-lead vocalist, co-songwriter, and rhythm guitarist of the Beatles. His work with the Beatles is celebrated for its impact on popular music.",
        "image": images[0]
    },
    {
        "name": "James Cameron",
        "bio": "James Cameron is a Canadian filmmaker known for his innovative use of technology in film. He directed the groundbreaking movies 'Avatar', 'Titanic', and 'The Terminator' series, among others. Cameron is celebrated for pushing the boundaries of visual effects and storytelling.",
        "image": images[1]
    },
    {
        "name": "Oprah Winfrey",
        "bio": "Oprah Winfrey is an American talk show host, television producer, actress, author, and philanthropist. She is best known for her talk show 'The Oprah Winfrey Show', which was the highest-rated television program of its kind. Oprah is recognized for her contributions to media and philanthropy.",
        "image": images[2]
    }
]
def generate_random_quote():
    ## generate_random_quote() is a helper method that generates a random quote and image to be displayed on the main page.
    n = len(images) - 1
    ## Generate a random number between 0 and n. We use this to index the lists of quotes and images. Each index is a different quote and image.
    index = random.randint(0, n)
    
    context = { "image": images[index], "quote": quotes[index] }
    return context 

def index(request:  HttpRequest) -> HttpResponse:
    """ index() method returns the main page, which will display a picture of a famous or notable person of your choosing 
    and a quote that this person said or wrote. The quote and image will be selected at random from a list of images/quote."""
    
    context = generate_random_quote()

    return render(request, "quotes/index.html", context)
    
    
    


def quote(request: HttpRequest) -> HttpResponse:
    """quote() method returns the same as /, to generate one quote and one image at random."""
    
    context = generate_random_quote()
    
    return render(request, "quotes/quote.html", context)


def show_all(request:HttpResponse) -> HttpResponse:
    """show_all() method returns an ancillary page which will show all quotes and images."""
    
    combined_list = [{'quote': quote, 'image': image} for quote, image in zip(quotes, images)]
    print(combined_list)
    
    context = { "combined": combined_list }
    
    return render(request, "quotes/show_all.html", context)


def about(request: HttpRequest) -> HttpResponse:
    """ about() method returns an about page with short biographical information about the person whose quotes you are displaying, as well as a note about the creator of this web application"""
    
    context = { "bio": celebs_bio }
    
    return render(request, "quotes/about.html", context)
