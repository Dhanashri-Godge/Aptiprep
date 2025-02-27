
from django.shortcuts import render
from .models import LeaderboardEntry

def global_leaderboard(request):
    # Retrieve all leaderboard entries (global view)
    entries = LeaderboardEntry.objects.all()
    context = {
        'entries': entries,
    }
    return render(request, 'leaderboard/global_leaderboard.html', context)
