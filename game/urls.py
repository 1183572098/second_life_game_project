from django.urls import path
from game import views


app_name = 'second_life'

urlpatterns = [
    path('', views.index, name='index'),
    path('initial/', views.initial_game, name='initial'),
    path('initial/random/', views.random_attribute, name='random'),
    path('initial/confirm/', views.game_confirm, name='confirm'),
]