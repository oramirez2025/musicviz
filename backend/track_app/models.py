from django.db import models

from user_app.models import UserProfile

class Track(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="tracks")
    spotify_id = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    lyrics = models.TextField(default="")

    def __str__(self):
        return f"{self.title} by {self.artist}"




