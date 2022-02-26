import json
from django.http import HttpResponse
from game.modules import game_manager, game_process
from game.modules import login_system


def index(request):
    print("This is index page")
    return HttpResponse("This is index Page. Testing")


def initial_game(request):
    data = json.loads(request.body.decode())
    manager = game_manager.Manager()
    result = manager.initial_game(data, game_process.Process())
    return HttpResponse(result)


def random_attribute(request):
    data = json.loads(request.body.decode())
    manager = game_manager.Manager()
    result = manager.random_attribute(data)
    return HttpResponse(result)


def game_confirm(request):
    data = json.loads(request.body.decode())
    manager = game_manager.Manager()
    result = manager.start_game(data)


def register(request):
    login_system.register(request)


def login(request):
    login_system.user_login(request)
