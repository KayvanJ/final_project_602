from django.shortcuts import render

# Create your views here.
import app.tmdb.api as tmd
import random

def home(request):
    movies = []
    while len(movies) < 12:
        mov = tmd.get_movie(random.randint(500,3000))
        if mov:
            movies.append(mov)

    return render(
                    request,
                    'app/index.html',
                    {
                       "movies": movies,
                    }
                )
                