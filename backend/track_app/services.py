import requests 

from .models import Track


def collect_artists(artists_obj):
    artists = ", ".join([a["name"] for a in artists_obj])
    return artists


def fetch_tracks(access_token):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50&offset=0"
    headers = {"Authorization" : f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    tracks = [{"spotify_id" : t["id"], "name": t["name"], "artists": collect_artists(t["artists"])} for t in data.get("items",[])]
    return tracks


def store_tracks(userProfile, tracks):
    for t in tracks:
        Track.objects.get_or_create(
            user = userProfile,
            spotify_id = t["spotify_id"],
            defaults={"name": t["name"], "artists": t["artists"]}
        )