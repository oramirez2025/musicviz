from django.urls import path
from .views import load_word_cloud


urlpatterns = [
   path('load_word_cloud', load_word_cloud.as_view(), name="load-word-cloud")
]


