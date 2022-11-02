from app.tmdb.models import Genre, Worker, ProdCompany, TMDBMovie
from datetime import datetime
import requests
import os

api_key = os.environ.get('TMDB')

def get_movie(id: int) -> TMDBMovie | None:
    response = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&append_to_response=credits")
    if response.status_code == 404:
        return

    json = response.json()
    poster = json.get("poster_path")
    backdrop = json.get("backdrop_path")
    if not poster or not backdrop:
        return

    genres: list[Genre] = []
    prods: list[ProdCompany] = []
    casts: list[Worker] = []
    crews: list[Worker] = []

    for genre in json.get("genres"):
        genres.append(Genre(genre["id"]))
    
    for prod in json.get("production_companies"):
        prods.append(ProdCompany(prod["id"]))
    
    creds = json.get("credits")
    if creds:
        for cast in creds.get("cast"):
            casts.append(
                Worker(
                    id=cast["id"], 
                    name=cast["name"], 
                    gender=cast["gender"], 
                    popularity=cast["popularity"],
                    task=cast["character"],
                    )
                )
        for crew in creds.get("crew"):
            crews.append(
                Worker(
                    id=crew["id"], 
                    name=crew["name"],
                    gender=crew["gender"],
                    popularity=crew["popularity"],
                    task=crew["job"],
                    )
                )
    
    date = datetime.strptime(json.get("release_date"), '%Y-%m-%d')
    movie = TMDBMovie(
        id = json.get("id"),
        poster = poster,
        backdrop = backdrop,
        status = json.get("status"),
        language = json.get("original_language"),
        title = json.get("original_title"),
        budget = json.get("budget"),
        runtime = json.get("runtime"),
        popularity = json.get("popularity"),
        revenue = json.get("revenue"),
        vote_count = json.get("vote_count"),
        vote_average = json.get("vote_average"),

        release_date = date,
        
        genres = genres,
        production_companies = prods,
        cast = casts,
        crew = crews
    )
    return  movie