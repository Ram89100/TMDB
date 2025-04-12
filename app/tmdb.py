import httpx
from app.config import TMDB_API_KEY

async def fetch_discover_movies():
    movies = []
    async with httpx.AsyncClient() as client:
        for page in range(1, 26): 
            res = await client.get("https://api.themoviedb.org/3/discover/movie", params={
                "api_key": TMDB_API_KEY,
                "page": page
            })
            res.raise_for_status()
            movies += res.json()["results"]
    return movies

async def fetch_movie_details(movie_id: int):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.themoviedb.org/3/movie/{movie_id}", params={
            "api_key": TMDB_API_KEY
        })
        res.raise_for_status()
        return res.json()

async def fetch_movie_credits(movie_id: int):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits", params={
            "api_key": TMDB_API_KEY
        })
        res.raise_for_status()
        return res.json()
