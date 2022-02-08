from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import git
import os


@csrf_exempt
def github_webhook(request):
    repo = git.Repo('./second_life_game_project')
    origin = repo.remotes.origin
    origin.pull()
    os.system('/var/www/caxiao_pythonanywhere_com_wsgi.py')
    print("reload web success!")
    return HttpResponse(status=200)
