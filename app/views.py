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
    299534,
    19995,
    324857  # Spider
]

movie_ids = [
    264419,
    1375,
    9873,
    426249,
    6071,
    337401,
    15975,
    146223,
    50116,
    9679,
    17708,
    64263
]


def home(request):
    if request.method == 'POST':
        query = request.POST['searchmovie'].replace(" ", "+")
        movies = tmd.search_db(query)
        print(movies)
    else:
        upcoming_movies = []
        for id in upcoming_ids:
            mov = tmd.get_movie(id)
            if mov:
                upcoming_movies.append(mov)

        best_movies = []
        for id in best_predictions:
            mov = tmd.get_movie(id)
            if mov:
                best_movies.append(mov)

        movies = []
        while len(movies) < 3:
            mov = tmd.get_movie(random.choice(movie_ids))
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
