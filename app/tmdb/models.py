from dataclasses import dataclass, field
from datetime import date
from app.tmdb.movie_predictor import MovieModel
import numpy as np
from datetime import datetime


movie_model = MovieModel()


@dataclass
class Genre:
    id: int
    name: str


@dataclass
class Worker:
    id: int
    name: str
    gender: bool
    popularity: float
    task: str


@dataclass
class ProdCompany:
    id: int


@dataclass
class TMDBMovie:
    id: int
    budget: int
    runtime: int
    revenue: int
    poster: str
    backdrop: str
    status: str
    language: str
    title: str
    vote_count: int
    popularity: float
    vote_average: float

    predicted_revenue: float

    release_date: date

    genres: list[Genre]
    production_companies: list[ProdCompany]
    cast: list[Worker] = field(repr=False)
    crew: list[Worker] = field(repr=False)

    lead_cast: list[Worker] = field(default_factory=list)
    lead_crew: list[Worker] = field(default_factory=list)

    def __post_init__(self):
        self.backdrop = f"https://image.tmdb.org/t/p/w500{self.backdrop}"
        self.poster = f"https://image.tmdb.org/t/p/w500{self.poster}"
        self.lead_cast = sorted(
            self.cast, key=lambda x: x.popularity, reverse=True)[:3]
        self.lead_crew = sorted(
            self.crew, key=lambda x: x.popularity, reverse=True)[:3]

        avg_budget = movie_model.dataframe['budget'].mean()
        std_budget = movie_model.dataframe['budget'].std()
        # avg_revenue = movie_model.df['revenue'].mean()
        # std_revenue = movie_model.df['revenue'].std()

        budget = self.budget if self.budget else 0
        money = (budget - avg_budget) / std_budget
        days = tryconvert(self.release_date)
        num_cast = len(self.cast)
        num_crew = len(self.crew)
        vote = self.vote_average
        voters = self.vote_count
        anomaly = 1 if self.revenue > (72287747*2) else 0

        data = np.array([money, voters, self.popularity,
                        anomaly]).reshape(-1, 1).T
        self.predicted_revenue = movie_model.predict(data)

    def __iter__(self):
        return iter(self.__dict__.items())


def tryconvert(date):
    try:
        return datetime.strptime(date, '%Y-%m-%d')
    except:
        return 0
