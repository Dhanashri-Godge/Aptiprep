from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.quiz_list, name="quiz_list"),  # View available quizzes
    path("create/", views.create_quiz, name="create_quiz"),  # Faculty creates quiz
    path("<int:quiz_id>/start/", views.start_quiz, name="start_quiz"),  # Student starts quiz
    path("<int:quiz_id>/submit/", views.submit_quiz, name="submit_quiz"),  # Student submits quiz
    path("<int:quiz_id>/result/", views.quiz_result, name="quiz_result"),  # View quiz result
]
