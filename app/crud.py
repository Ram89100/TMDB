from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app import models

def save_movie(db: Session, details: dict, credits: dict):
    if db.query(models.Movie).filter(models.Movie.id == details["id"]).first():
        return

    movie = models.Movie(
        id=details["id"],
        title=details.get("title"),
        release_date=details.get("release_date"),
        popularity=details.get("popularity"),
        vote_average=details.get("vote_average"),
        vote_count=details.get("vote_count"),
        revenue=details.get("revenue") or 0
    )

    for g in details.get("genres", []):
        genre = db.query(models.Genre).get(g["id"]) or models.Genre(id=g["id"], name=g["name"])
        movie.genres.append(genre)

    for c in credits.get("cast", [])[:5]:
        cast = db.query(models.Cast).get(c["id"]) or models.Cast(id=c["id"], name=c["name"])
        movie.cast.append(cast)

    db.add(movie)
    db.commit()

def get_movies(db: Session, year, genres, without_genres, search, sort_by, order, page, page_size):
    q = db.query(models.Movie)

    if year:
        q = q.filter(models.Movie.release_date.like(f"{year}%"))
    if genres:
        q = q.filter(models.Movie.genres.any(models.Genre.id.in_(genres)))
    if without_genres:
        q = q.filter(~models.Movie.genres.any(models.Genre.id.in_(without_genres)))
    if search:
        q = q.filter(or_(
            models.Movie.title.ilike(f"%{search}%"),
            models.Movie.cast.any(models.Cast.name.ilike(f"%{search}%"))
        ))

    sort_attr = getattr(models.Movie, sort_by)
    q = q.order_by(desc(sort_attr) if order == "desc" else asc(sort_attr))
    return q.offset((page - 1) * page_size).limit(page_size).all()
