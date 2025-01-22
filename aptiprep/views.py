from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages as message
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    return render(request, 'index.html')


def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        if password==password2:
            if User.objects.filter(username=username).exists():
                message.info(request, 'Username taken')
                return render(request, 'sign_up.html')
            elif User.objects.filter(email=email).exists():
                message.info(request, 'Email taken')
                return render(request, 'sign_up.html')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                user.save()
                message.info(request, 'User created')
                return render(request, 'index.html')

        else:
            message.warning(request, 'Passwords not matching')
            return render(request, 'sign_up.html')
    else:
        return render(request, 'sign_up.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            message.info(request, 'login succesfull')
            return redirect('dashboard')
        else:
            message.error(request, 'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
    
def logout(request):
        auth.logout(request)
        return render(request, 'index.html')
def dashboard(request):
    return render(request, 'dashboard.html')

def create_quiz(request):
    return render(request, 'create_quiz.html')


from .forms import QuestionForm, OptionFormSet

def create_quiz(request):
    if request.method == 'POST':
        num_questions = int(request.POST.get('num_questions', 1))
        question_forms = []
        for i in range(num_questions):
            question_form = QuestionForm(request.POST, prefix=f'question_{i}')
            option_form_set = OptionFormSet(request.POST, prefix=f'options_{i}')
            question_forms.append((question_form, option_form_set))
        
        # Handle form validation and saving here

    else:
        question_forms = [(QuestionForm(prefix=f'question_{i}'), OptionFormSet(prefix=f'options_{i}')) for i in range(1)]

    return render(request, 'create_quiz.html', {'question_forms': question_forms})




@login_required
def dashboard(request):
    # Replace with logic to calculate tests given
    tests_given = 5  # Example value; replace with dynamic data

    context = {
        'tests_given': tests_given,
    }
    return render(request, 'dashboard.html', context)
