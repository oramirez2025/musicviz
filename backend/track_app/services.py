import requests


from rest_framework.response import Response
from .models import Track


from django.conf import settings
import re

from lyricsgenius import Genius

genius = Genius(settings.GENIUS_ACCESS_TOKEN)



def collect_artists(artists_obj):
   """
   A class to represent a person.

   ...

   Attributes
   ----------
   name : str
      first name of the person
   surname : str
      family name of the person
   age : int
      age of the person

   Methods
   -------
   info(additional=""):
      Prints the person's name and age.
   """
   artists = ", ".join([a["name"].lower() for a in artists_obj])
   return artists





# some songs have extra text to them such as "Remastered", which messes with the
# search of the Genius API

# as of now the only example I can think of -
def clean_name(name):
   return name.split("-")[0].strip().lower()
  

def collect_lyrics(artists, name):
   try:
      lyrics = genius.search_song(title=name, artist=artists).lyrics
      cleaned_lyrics = re.sub(r'\[.*?\]', '', lyrics)
      cleaned_lyrics = re.sub(r'[(),\\?!"-]+', '', cleaned_lyrics)
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
   return tracks


def store_tracks(userProfile, tracks):
   for t in tracks:
       Track.objects.update_or_create(
           user = userProfile,
           spotify_id = t["spotify_id"],
           defaults={"artist" : t["artists"], "name" : t["name"], "lyrics" : t["lyrics"]}
       )
