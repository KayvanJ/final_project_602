from django.shortcuts import render

# Create your views here.
import app.tmdb.api as tmd

def home(request):
    x = tmd.get_movie(550)
    print(x.content)
    return render(request, 'app/index.html')