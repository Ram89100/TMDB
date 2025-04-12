from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas, crud, tmdb

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="TMDB Movie Explorer")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/populate")
async def populate(db: Session = Depends(get_db)):
    movies = await tmdb.fetch_discover_movies()
    for movie in movies:
        details = await tmdb.fetch_movie_details(movie["id"])
        credits = await tmdb.fetch_movie_credits(movie["id"])
        crud.save_movie(db, details, credits)
    return {"message": "Populated 500 movies"}

@app.get("/movies", response_model=list[schemas.MovieOut])
def get_movies(
    year: int = Query(None),
    genres: list[int] = Query(None),
    without_genres: list[int] = Query(None),
    search: str = Query(None),
    sort_by: str = Query("popularity"),
    order: str = Query("desc"),
    page: int = Query(1),
    page_size: int = Query(20),
    db: Session = Depends(get_db)
):
    return crud.get_movies(db, year, genres, without_genres, search, sort_by, order, page, page_size)
