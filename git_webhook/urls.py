from django.urls import path
from git_webhook import views


app_name = 'git_webhook'

urlpatterns = [
    path('', views.github_webhook, name='github_webhook'),
]