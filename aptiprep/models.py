

# Create your models here.
from django.db import models
import uuid

class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=200)
    question_marks = models.IntegerField()

    def __str__(self):
        return self.question_text


class Option(models.Model):
    option_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")

    def __str__(self):
        return self.option_text
