from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

movie_genre = Table('movie_genre', Base.metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

movie_cast = Table('movie_cast', Base.metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('cast_id', ForeignKey('casts.id'))
)

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)
    popularity = Column(Float)
    vote_average = Column(Float)
    vote_count = Column(Integer)
    revenue = Column(Integer)

    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    cast = relationship("Cast", secondary=movie_cast, back_populates="movies")

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")

class Cast(Base):
    __tablename__ = 'casts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship("Movie", secondary=movie_cast, back_populates="cast")
