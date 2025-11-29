import requests 

from .models import Track
from bs4 import BeautifulSoup

from django.conf import settings
import re 


def collect_artists(artists_obj):
    artists = ", ".join([a["name"] for a in artists_obj])
    return artists


def scrape_lyrics(title, artists):
    # use Genius API to get the page for the lyrics
    base_url = "https://api.genius.com"
    headers = {"Authorization" : f"Bearer {settings.GENIUS_ACCESS_TOKEN}"}
    search_url = f"{base_url}/search"
    data = {"q": f"{title} {artists}"}
    response = requests.get(search_url, data=data, headers=headers)
    song_data = response.json()["response"]["hits"][0]["result"]

    # from the lyrics page, scrape the lyrics of the song
    lyrics_page_url = song_data["url"]
    page = requests.get(lyrics_page_url)
    html = BeautifulSoup(page.text, "html.parser")
    lyrics_divs = html.find_all("div", attrs={"data-lyrics-container": "true"})
    lyrics = ""
    for t in lyrics_divs:
        lyrics += t.get_text(" ")
    # clean up lyrics - seems like there's some extra stuff at the beginning then those [...]
    first = re.search(r'\[.*?\]', lyrics)
    index = first.end()
    cleaned_lyrics = re.sub(r'\[.*?\]', '', lyrics[index:])
    return cleaned_lyrics

def fetch_tracks(access_token):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50&offset=0"
    headers = {"Authorization" : f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    tracks = [{"spotify_id" : t["id"], "name": t["name"], 
               "artists": collect_artists(t["artists"])} for t in data.get("items",[])]
    for t in tracks:
        tracks["lyrics"] = scrape_lyrics(t["name"], t["artists"])
    return tracks


def store_tracks(userProfile, tracks):
    for t in tracks:
        Track.objects.get_or_create(
            user = userProfile,
            spotify_id = t["spotify_id"],
            defaults={"name": t["name"], "artists": t["artists"], "lyrics": t["lyrics"]}
        )