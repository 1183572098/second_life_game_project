from django.urls import path
from game import views


app_name = 'second_life'

urlpatterns = [
    path('', views.index, name='index'),
]