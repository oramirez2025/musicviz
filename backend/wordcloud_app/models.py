from django.db import models


from user_app.models import UserProfile


class WordCloud(models.Model):
   user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="WordCloud")
   words = models.JSONField()