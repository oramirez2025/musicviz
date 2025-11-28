from django.db import models

from user_app.models import UserProfile

class Track(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} by {self.artist}"




