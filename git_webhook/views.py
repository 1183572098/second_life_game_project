from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import git
import os


@csrf_exempt
def github_webhook(request):
    repo = git.Repo('./second_life_game_project')
    origin = repo.remotes.origin
    repo.git.reset('--hard')
    origin.pull()
    os.utime('/var/www/caxiao_pythonanywhere_com_wsgi.py', None)
    print("reload web success!")
    return HttpResponse(status=200)
