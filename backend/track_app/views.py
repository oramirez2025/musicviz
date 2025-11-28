from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from .services import *

class TopTrackView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        userProfile = request.user.userprofile
        tracks = fetch_tracks(userProfile.access_token)
        store_tracks(userProfile,tracks)
        return Response(tracks)

        