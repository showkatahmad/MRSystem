from django.shortcuts import render
from .models import *


# Create your views here.
def home(request):
    movies = Movie.objects.all() 
    
    context = {
        'movies' : movies

    }
    return render(request, 'recommendation/home.html', context)