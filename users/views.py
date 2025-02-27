from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth.decorators import login_required
from quizzes.models import Quiz, QuizAttempt

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserLoginForm


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User registered successfully")
            login(request, user)  # Auto-login after registration
            messages.success(request, "Registration successful!")
            return redirect("home")  # Adjust this redirect as needed
        else:
            print("Form errors:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            print("Cleaned data:", form.cleaned_data)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                print("Login successful")
                messages.success(request, "Login successful!")
                return redirect("profile")  # Adjust this redirect as needed
            else:
                print("Invalid username or password")
                messages.error(request, "Invalid username or password.")
        else:
            print("Form validation errors:", form.errors)
    else:
        print("GET request received for login page.")
        form = CustomUserLoginForm()
    return render(request, "users/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


@login_required
def profile_view(request):
    user = request.user
    context = {"user": user}
    
    if user.role == "student":
        quiz_attempts = QuizAttempt.objects.filter(user=user)
        total_tests = quiz_attempts.count()
        total_score = sum(attempt.score for attempt in quiz_attempts)
        average_score = total_score / total_tests if total_tests > 0 else 0
        rank = None  # We can implement ranking logic later

        context.update({
            "total_tests": total_tests,
            "average_score": average_score,
            "rank": rank,
            "recent_quizzes": quiz_attempts.order_by("-attempted_at")[:5]
,
        })

    elif user.role == "faculty":
        hosted_quizzes = Quiz.objects.filter(created_by=user)
        total_quizzes = hosted_quizzes.count()
        total_attempts = sum(quiz.attempts.count() for quiz in hosted_quizzes)
        
        context.update({
            "total_quizzes": total_quizzes,
            "total_attempts": total_attempts,
            "hosted_quizzes": hosted_quizzes,
        })

    return render(request, "users/profile.html", context)

