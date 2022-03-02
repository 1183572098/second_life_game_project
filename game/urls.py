from django.urls import path
from game import views


app_name = 'second_life'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('initial/', views.initial_game, name='initial'),
    path('initial/random/', views.random_attribute, name='random'),
    path('initial/confirm/', views.game_confirm, name='confirm'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('start/', views.start_game, name='startgame')
]