from pydantic import BaseModel
from typing import List, Optional

class Genre(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Cast(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class MovieOut(BaseModel):
    id: int
    title: str
    release_date: Optional[str]
    popularity: Optional[float]
    vote_average: Optional[float]
    vote_count: Optional[int]
    revenue: Optional[int]
    genres: List[Genre] = []
    cast: List[Cast] = []

    class Config:
        orm_mode = True
