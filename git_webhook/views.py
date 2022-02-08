from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import git


@csrf_exempt
def github_webhook(request):
    repo = git.Repo('./second_life_game_project')
    origin = repo.remotes.origin
    print(origin.pull())
    return HttpResponse(status=200)
