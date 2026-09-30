"""Scrape popular and trending movie names from multiple web sources."""
import re
import sys
import time
from pathlib import Path
from typing import List, Optional
from bs4 import BeautifulSoup
import requests

# Add 'src' to python path
src_path = Path(__file__).resolve().parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from jarvis.config import PROJECT_ROOT

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

UNWANTED_KEYWORDS = [
    'box office', 'collection', 'review', 'trailer', 'teaser', 'first look', 'poster',
    'release date', 'cast', 'budget', 'recently viewed', 'latest', 'upcoming', 'news',
    'updates', 'photos', 'videos', 'songs', 'music', 'interview', 'screening',
    'premiere', 'celebrity', 'star cast', 'download', 'watch online', 'in cinemas',
    'full movie', 'official', 'hd', '4k', 'movie online', 'film online', 'streaming',
    'now playing', 'available on', 'digital release', 'on netflix', 'on amazon prime',
    'on disney plus', 'on hulu', 'on hotstar', 'on zee5', 'on sony liv', 'on alt balaji',
    'on mx player', 'on voot', 'part 1', 'part 2', 'chapter 1', 'chapter 2', 'season 1',
    'season 2', 's1', 's2', 'episode 1', 'episode 2', 'ep 1', 'ep 2', 'full hd',
    'hdrip', 'brrip', 'dvdrip', 'webrip', 'web-dl', 'camrip', 'ts', 'tc', 'hdts',
    'hdcam', 'bluray', 'blu-ray', '4k uhd', 'remastered', "director's cut",
    'extended edition', 'special edition', 'uncut', 'unrated', 'subtitled', 'dubbed',
    'with subtitles', 'with english subtitles', 'with hindi subtitles', 'hindi dubbed',
    'english dubbed'
]

def clean_movie_name(title: str) -> Optional[str]:
    """Clean movie name by filtering unwanted words, years, and suffixes."""
    title_lower = title.lower()
    for kw in UNWANTED_KEYWORDS:
        if kw in title_lower:
            return None

    title = re.sub(r"\s+(movie|film|english|hindi|telugu|tamil|malayalam|kannada)$", "", title, flags=re.IGNORECASE)
    title = re.sub(r"\s*[\(\[]?\d{4}[\)\]]?\s*", " ", title)
    title = " ".join(title.split()).strip()
    return title if len(title) > 1 else None

def get_imdb_popular_movies() -> List[str]:
    movies = []
    try:
        url = "https://www.imdb.com/chart/moviemeter/"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        for el in soup.find_all("h3", class_="ipc-title__text"):
            text = el.get_text(strip=True)
            if ". " in text:
                text = text.split(". ", 1)[1]
            cleaned = clean_movie_name(text)
            if cleaned:
                movies.append(cleaned)
        print(f"✓ IMDb Popular: {len(movies)} movies")
    except Exception as e:
        print(f"✗ IMDb Popular Error: {e}")
    return movies

def get_imdb_top250() -> List[str]:
    movies = []
    try:
        url = "https://www.imdb.com/chart/top/"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        for el in soup.find_all("h3", class_="ipc-title__text"):
            text = el.get_text(strip=True)
            if ". " in text:
                text = text.split(". ", 1)[1]
            cleaned = clean_movie_name(text)
            if cleaned:
                movies.append(cleaned)
        print(f"✓ IMDb Top 250: {len(movies)} movies")
    except Exception as e:
        print(f"✗ IMDb Top 250 Error: {e}")
    return movies

def get_letterboxd_popular() -> List[str]:
    movies = []
    try:
        url = "https://letterboxd.com/films/popular/this/week/"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        for img in soup.find_all("img", class_="image"):
            alt = img.get("alt")
            if alt:
                cleaned = clean_movie_name(alt)
                if cleaned:
                    movies.append(cleaned)
        print(f"✓ Letterboxd Popular: {len(movies)} movies")
    except Exception as e:
        print(f"✗ Letterboxd Error: {e}")
    return movies

def get_tmdb_popular() -> List[str]:
    movies = []
    try:
        url = "https://www.themoviedb.org/movie"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        for link in soup.find_all("a", class_="title"):
            title = link.get_text(strip=True)
            cleaned = clean_movie_name(title)
            if cleaned:
                movies.append(cleaned)
        print(f"✓ TMDB: {len(movies)} movies")
    except Exception as e:
        print(f"✗ TMDB Error: {e}")
    return movies

def remove_duplicates(movie_list: List[str]) -> List[str]:
    seen = set()
    unique = []
    for m in movie_list:
        clean = m.strip()
        lower = clean.lower()
        if lower not in seen and len(clean) >= 2:
            seen.add(lower)
            unique.append(clean)
    return unique

def main():
    print("=" * 60)
    print("SCRAPING MOVIE NAMES")
    print("=" * 60)
    all_movies = []
    all_movies.extend(get_imdb_popular_movies())
    time.sleep(1)
    all_movies.extend(get_imdb_top250())
    time.sleep(1)
    all_movies.extend(get_letterboxd_popular())
    time.sleep(1)
    all_movies.extend(get_tmdb_popular())

    unique_movies = remove_duplicates(all_movies)
    output_path = PROJECT_ROOT / "movies.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        for m in unique_movies:
            f.write(f"{m}\n")
    print(f"\n✓ Saved {len(unique_movies)} unique movies to '{output_path}'")

if __name__ == "__main__":
    main()
