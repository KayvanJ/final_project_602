from django.shortcuts import render

# Create your views here.
import app.tmdb.api as tmd
import random

upcoming_ids = [
    76600,
    609681,
    615777,
]

best_predictions = [
    324857,
    64263,
    254470,
    7840,
]

movie_ids = [
    505642,
    1374,
    114150,
    426249,
    6071,
    337401,
    15975,
    146223,
    50116,
    17708,
    829799,
]


def home(request):
    upcoming_movies = []
    best_movies = []
    movies = []

    if request.method == 'POST':
        query = request.POST['searchmovie'].replace(" ", "+")
        movies = tmd.search_db(query)
    else:
        for id in upcoming_ids:
            mov = tmd.get_movie(id)
            if mov:
                upcoming_movies.append(mov)

        for id in best_predictions:
            mov = tmd.get_movie(id)
            if mov:
                best_movies.append(mov)

        for id in movie_ids:
            mov = tmd.get_movie(id)
            if mov:
                movies.append(mov)
    return render(
        request,
        'app/index.html',
        {
            "upcoming_movies": upcoming_movies,
            "best_movies": best_movies,
            "movies": movies,
        }
    )


def loading(request):
    return render(
        request,
        'app/loading.html',
    )
