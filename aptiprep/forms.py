from django import forms
from .models import Question, Option
from django.forms import inlineformset_factory

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'question_marks']

OptionFormSet = inlineformset_factory(Question, Option, fields=['option_text', 'is_correct'], extra=3)