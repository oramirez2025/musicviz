import requests




from rest_framework.response import Response
from .models import Track
# from bs4 import BeautifulSoup


from django.conf import settings
import re

from lyricsgenius import Genius

genius = Genius(settings.GENIUS_ACCESS_TOKEN)




def collect_artists(artists_obj):
   artists = ", ".join([a["name"].lower() for a in artists_obj])
   return artists




# def scrape_lyrics(title, artists):
#    # use Genius API to get the page for the lyrics
#    base_url = "https://api.genius.com"
#    headers = {"Authorization" : f"Bearer {settings.GENIUS_ACCESS_TOKEN}"}
#    search_url = f"{base_url}/search"
#    params = {"q": f"{title} {artists}"}
  
#    try:
#        response = requests.get(search_url, params=params, headers=headers)
#        hits = response.json()["response"]["hits"]
#        song_data = None
#        first_artist = artists.split(",")[0]
#        # print(first_artist)
#        for i in range(len(hits)):
#            if first_artist in hits[i]["result"]["artist_names"].lower():
#                song_data = hits[i]["result"]
#                break
#        # from the lyrics page, scrape the lyrics of the song
#        lyrics_page_url = song_data["url"]
#        # print(f"scraping {title} {artists} gave this: {lyrics_page_url}")
#        page = requests.get(lyrics_page_url)
#        html = BeautifulSoup(page.text, "html.parser")
#     #    print(html)
#        lyrics_divs = html.find_all("div", attrs={"data-lyrics-container": "true"})
#        for i in range(len(lyrics_divs)):
#            div = lyrics_divs[i]
#            print(f"the {i}th div is {div.text}\n")
#        lyrics = " ".join(div.get_text(" ") for div in lyrics_divs)
#        # clean up lyrics - seems like there's some extra stuff at the beginning then those [...]
#        index_1 = re.search(r'\[.*?\]', lyrics).end() if re.search(r'\[.*?\]', lyrics) else -1
#        index_2 = re.search("Lyrics", lyrics).end() if re.search("Lyrics", lyrics) else -1
#        if index_1 or index_2:
#            index = max(index_1,index_2)
#            cleaned_lyrics = re.sub(r'\[.*?\]', '', lyrics[index:])
#            cleaned_lyrics = re.sub(r'[()]+', '', cleaned_lyrics)
#            return cleaned_lyrics.strip()
#        else:
#            cleaned_lyrics = re.sub(r'\[.*?\]', '', lyrics)
#            cleaned_lyrics = re.sub(r'[()]+', '', cleaned_lyrics)
#            return cleaned_lyrics.strip()
#    except Exception as e:
#        print(f"error with scraping {title} {artists}: {e}")
#        return ""
  
# some songs have extra text to them such as "Remastered", which messes with the
# search of the Genius API


# as of now the only example I can think of -
def clean_name(name):
   return name.split("-")[0].strip().lower()
  

def collect_lyrics(artists, name):
   try:
      lyrics = genius.search_song(title=name, artist=artists).lyrics
      cleaned_lyrics = re.sub(r'\[.*?\]', '', lyrics)
      cleaned_lyrics = re.sub(r'[()]+', '', cleaned_lyrics)
      cleaned_lyrics = re.sub(r'\n', ' ', cleaned_lyrics)
      return cleaned_lyrics.strip()
   except Exception as e:
      return ""


def fetch_tracks(access_token):
   url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50&offset=0"
   headers = {"Authorization" : f"Bearer {access_token}"}
   response = requests.get(url, headers=headers)
   data = response.json()
   tracks = [{"spotify_id" : t["id"], "name": clean_name(t["name"]),
              "artists": collect_artists(t["artists"]),
              "lyrics": collect_lyrics(t["artists"][0]["name"].lower(), clean_name(t["name"]))} for t in data.get("items",[])]
  
#    for i in range(len(tracks)):
#        tracks[i]["lyrics"] = scrape_lyrics(tracks[i]["name"],tracks[i]["artists"])
   return tracks


def store_tracks(userProfile, tracks):
   for t in tracks:
       Track.objects.update_or_create(
           user = userProfile,
           spotify_id = t["spotify_id"],
           defaults={"artist" : t["artists"], "name" : t["name"], "lyrics" : t["lyrics"]}
       )








# TESTING:
# from rest_framework.decorators import api_view
# @api_view(["GET"])
# def fetch_lyrics(request):
#    try:
#        lyrics = scrape_lyrics("the bed took fire","morrissey")
#        return Response({"lyrics": lyrics})
#    except Exception as e:
#        print(e)
#        return Response("bad")
