import requests
import os

api_key = os.environ.get('TMDB')

def get_movie(id: int):
    return requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}")