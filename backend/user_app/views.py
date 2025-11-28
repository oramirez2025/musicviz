from django.shortcuts import render
import urllib.parse
from django.conf import settings
from django.shortcuts import redirect
import requests
from .models import UserProfile
from django.contrib.auth.models import User

from django.contrib.auth import login


def spotify_login(request):
    scopes = "user-read-recently-played user-top-read"
    query_params = {
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": scopes
    }
    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(query_params)
    return redirect(url)

def spotify_callback(request):
    code = request.GET.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
    "client_id": settings.SPOTIFY_CLIENT_ID,
    "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=payload)
    data = response.json()
    
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    user_data = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    spotify_id = user_data["id"]
    user, created = User.objects.get_or_create(username=spotify_id)

    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.spotify_id = spotify_id
    profile.access_token = access_token
    profile.refresh_token = refresh_token
    profile.save()

    login(request, user)

    return redirect("/")



