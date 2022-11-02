from dataclasses import dataclass, field
from datetime import date

@dataclass
class Genre:
    id: int

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
        self.lead_cast = sorted(self.cast, key=lambda x: x.popularity, reverse=True)[:6]
        self.lead_crew = sorted(self.crew, key=lambda x: x.popularity, reverse=True)[:6]
    
    def __iter__(self):
        return iter(self.__dict__.items())


    
