from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

import matplotlib
import matplotlib.pyplot as plt
import io
import urllib, base64

from collections import Counter

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Leidy Roldan'}) 
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        Movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        Movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':Movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics(request):
    matplotlib.use('Agg')

    # Gráfica 1: películas por año
    all_movies = Movie.objects.all()

    movie_count_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_count_by_year[year] = movie_count_by_year.get(year, 0) + 1

    bar_positions = range(len(movie_count_by_year))

    plt.figure(figsize=(10, 5))
    plt.bar(bar_positions, movie_count_by_year.values(), width=0.5, align='center')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, movie_count_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # ráfica 2: películas por género (solo primer género)
    all_genres = Movie.objects.values_list('genre', flat=True)

    first_genres = []
    for g in all_genres:
        if g:
            first = g.split(',')[0].strip()
            if first:
                first_genres.append(first)

    genre_counts = Counter(first_genres)
    genre_counts = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True))

    plt.figure(figsize=(10, 5))
    plt.bar(genre_counts.keys(), genre_counts.values())
    plt.title('Movies per genre (first only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()

    image_png2 = buffer2.getvalue()
    buffer2.close()
    graphic_genre = base64.b64encode(image_png2).decode('utf-8')

    # Renderizar template con ambas gráficas
    return render(request, 'statistics.html', {
        'graphic': graphic,
        'graphic_genre': graphic_genre
    })