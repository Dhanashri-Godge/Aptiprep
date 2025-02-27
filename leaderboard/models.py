# leaderboard/models.py
from django.db import models
from users.models import CustomUser

class LeaderboardEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    num_tests = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    # Optional fields for future filtering:
    category = models.CharField(max_length=100, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_score', '-average_score']

    def __str__(self):
        return f"{self.user.name} - Score: {self.total_score}"

