from django.shortcuts import render

# Create your views here.
import app.tmdb.api as tmd
import random

valid_ids = [
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
        movies = []
        while len(movies) < 2:
            mov = tmd.get_movie(random.randint(1, 1000000))
            if mov:
                movies.append(mov)

    return render(
        request,
        'app/index.html',
        {
            "movies": movies,
        }
    )


def loading(request):
    return render(
        request,
        'app/loading.html',
    )
