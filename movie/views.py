from django.shortcuts import render
from django.http import HttpResponse

from .models import MOvie

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Leidy Roldan'}) 
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        Movie = MOvie.objects.filter(title__icontains=searchTerm)
    else:
        Movie = MOvie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':Movie})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')
