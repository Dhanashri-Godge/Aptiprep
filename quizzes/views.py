from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Quiz, Question, Option, QuizAttempt
from users.models import CustomUser

#  List available quizzes
#@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, "quizzes/quiz_list.html", {"quizzes": quizzes})

# Faculty can create a quiz
#@login_required
def create_quiz(request):
    if request.user.role != "faculty":
        return redirect("quiz_list")

    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")
        duration = request.POST.get("duration")
        
        quiz = Quiz.objects.create(
            title=title, category=category, duration=duration, created_by=request.user
        )
        return redirect("quiz_list")
    
    return render(request, "quizzes/create_quiz.html")

#  Student starts a quiz
#@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, "quizzes/start_quiz.html", {"quiz": quiz, "questions": questions})

#  Student submits quiz
#@login_required
def submit_quiz(request, quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        score = 0

        for question in questions:
            selected_option_id = request.POST.get(f"question_{question.id}")
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                if selected_option.is_correct:
                    score += 1

        QuizAttempt.objects.create(user=request.user, quiz=quiz, score=score)
        return redirect("quiz_result", quiz_id=quiz_id)

    return redirect("quiz_list")

#  View quiz result
#@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).first()
    
    return render(request, "quizzes/quiz_result.html", {"quiz": quiz, "attempt": attempt})
