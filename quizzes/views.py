from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Quiz, Question, Option, QuizAttempt
from users.models import CustomUser

#  List available quizzes
@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, "quizzes/quiz_list.html", {"quizzes": quizzes})

# Faculty can create a quiz
@login_required
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
@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, "quizzes/start_quiz.html", {"quiz": quiz, "questions": questions})

#  Student submits quizfrom django.shortcuts import render, get_object_or_404, redirect


def serialize_question_results(results):
    """
    Convert question result objects into a serializable list of dictionaries.
    Each dictionary contains:
      - question_text
      - selected_option_text
      - correct_option_text
      - is_correct (boolean)
      - explanation (if any)
    """
    serialized = []
    for result in results:
        serialized.append({
            'question_text': result['question'].text,
            'selected_option_text': result['selected_option'].text if result['selected_option'] else "No Answer",
            'correct_option_text': result['correct_option'].text if result['correct_option'] else "N/A",
            'is_correct': result['is_correct'],
           
        })
    return serialized

@login_required
def submit_quiz(request, quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        score = 0
        question_results = []  # List to store details for each question

        for question in questions:
            selected_option_id = request.POST.get(f"question_{question.id}")
            selected_option = None
            is_correct = False
            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=selected_option_id)
                    if selected_option.is_correct:
                        score += 1
                        is_correct = True
                except Option.DoesNotExist:
                    selected_option = None
            # Get the correct option for the question (assuming only one correct option)
            correct_option = question.options.filter(is_correct=True).first()
            question_results.append({
                'question': question,
                'selected_option': selected_option,
                'correct_option': correct_option,
                'is_correct': is_correct
            })

        QuizAttempt.objects.create(user=request.user, quiz=quiz, score=score)
        
        # Serialize the detailed results and store in session for the result page.
        request.session['question_results'] = serialize_question_results(question_results)
        request.session['total_questions'] = questions.count()
        
        return redirect("quiz_result", quiz_id=quiz.id)

    return redirect("quiz_list")

@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # Retrieve the latest attempt for this quiz by the user.
    attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by("-attempted_at").first()
    
    # Get detailed results from the session.
    total_questions = request.session.get('total_questions', 0)
    question_results = request.session.get('question_results', [])
    
    # Optionally, clear the session data after using it.
    request.session.pop('question_results', None)
    request.session.pop('total_questions', None)
    
    return render(request, "quizzes/quiz_result.html", {
        "quiz": quiz,
        "attempt": attempt,
        "total_questions": total_questions,
        "question_results": question_results
    })





# Faculty can add questions to a quiz
@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.user.role != "faculty":
        return redirect("quiz_list")

    if request.method == "POST":
        question_text = request.POST.get("question_text")
        question = Question.objects.create(quiz=quiz, text=question_text)
        return redirect("add_options", question_id=question.id)

    return render(request, "quizzes/add_question.html", {"quiz": quiz})

# Faculty can add options to a question
@login_required
def add_options(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.user.role != "faculty":
        return redirect("quiz_list")

    if request.method == "POST":
        option_text = request.POST.get("option_text")
        is_correct = request.POST.get("is_correct") == "on"  # Checkbox for marking correct answer

        Option.objects.create(question=question, text=option_text, is_correct=is_correct)
        return redirect("add_options", question_id=question.id)  # Stay on page to add more options

    return render(request, "quizzes/add_options.html", {"question": question})

