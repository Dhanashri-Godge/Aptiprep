from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up/', views.signUp, name='sign_up'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
     path('create-quiz/', views.create_quiz, name='create_quiz'),
     path('dashboard/', views.dashboard, name='dashboard'),
]
