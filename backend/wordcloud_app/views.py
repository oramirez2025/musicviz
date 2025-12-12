from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .services import create_word_freq
from .serializers import WordCloudSerializer




class load_word_cloud(APIView):
   permission_classes = [IsAuthenticated]
   def get(self,request):
       user = request.user.userprofile
       wc = WordCloudSerializer(create_word_freq(user))
       return Response(wc.data)