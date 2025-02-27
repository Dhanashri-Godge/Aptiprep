# leaderboard/urls.py
from django.urls import path
from .views import global_leaderboard

urlpatterns = [
    path("global/", global_leaderboard, name="global_leaderboard"),
]
