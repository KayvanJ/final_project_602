from app.tmdb.models import Genre, Worker, ProdCompany, TMDBMovie
from datetime import datetime
import requests
import os

api_key = os.environ.get('TMDB')


def search_db(query: str):
    movies = []
    response = requests.get(
        f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    )
    if response.status_code == 404:
        return movies

    json = response.json()
    if json['results']:
        for movie in json['results']:
            mov = get_movie(id=movie.get('id'))
            if mov:
                movies.append(mov)

    return movies


def get_movie(id: int) -> TMDBMovie | None:
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&append_to_response=credits")
    if response.status_code == 404:
        return

    json = response.json()
    if json.get("adult"):
        return
    if json.get("revenue") == 0:
        return

    poster = json.get("poster_path")
    backdrop = json.get("backdrop_path")
    if not poster or not backdrop:
        return

    genres: list[Genre] = []
    prods: list[ProdCompany] = []
    casts: list[Worker] = []
    crews: list[Worker] = []

    for genre in json.get("genres"):
        genres.append(Genre(genre["id"], genre["name"]))

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

    try:
        date = datetime.strptime(json.get("release_date"), '%Y-%m-%d')
    except:
        date = datetime.now() - 1

    movie = TMDBMovie(
        id=json.get("id"),
        poster=poster,
        backdrop=backdrop,
        status=json.get("status"),
        language=json.get("original_language"),
        title=json.get("original_title"),
        budget=json.get("budget"),
        runtime=json.get("runtime"),
        popularity=json.get("popularity"),
        revenue=json.get("revenue"),
        vote_count=json.get("vote_count"),
        vote_average=json.get("vote_average"),
        predicted_revenue=0,

        release_date=date,

        genres=genres,
        production_companies=prods,
        cast=casts,
        crew=crews
    )
    return movie
