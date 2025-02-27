from django.db import models
from users.models import CustomUser

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=[("Aptitude", "Aptitude"), ("Coding", "Coding"), ("Logical", "Logical")])
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'faculty'})
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=[("MCQ", "MCQ"), ("True/False", "True/False")])

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - Score: {self.score}"
