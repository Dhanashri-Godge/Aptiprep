from django.shortcuts import render
from quizzes.models import QuizAttempt
from django.db.models import Avg, Sum, Count

def dashboard(request):
    user = request.user
    # Get all quiz attempts for the current user
    attempts = QuizAttempt.objects.filter(user=user)
    
    # Aggregate statistics
    total_tests = attempts.count()
    average_score = attempts.aggregate(avg=Avg('score'))['avg'] or 0
    total_score = attempts.aggregate(total=Sum('score'))['total'] or 0
    
    context = {
        'total_tests': total_tests,
        'average_score': round(average_score, 2),
        'total_score': total_score,
        'attempts': attempts.order_by('-attempted_at')[:5],  # recent 5 attempts
    }
    
    return render(request, 'analytics/dashboard.html', context)
