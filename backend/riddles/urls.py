# app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'riddles'

urlpatterns = [
    path('', views.riddles_list, name='riddles_list'), #maps  to the views.riddle_list
    path('submit_answer/<int:riddle_id>/', views.submit_answer, name='submit_answer'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),


    
    # other URL patterns for this app
]
