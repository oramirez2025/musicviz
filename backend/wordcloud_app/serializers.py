from rest_framework import serializers
from .models import WordCloud


class WordCloudSerializer(serializers.ModelSerializer):
   class Meta:
       model = WordCloud
       fields = ['words']