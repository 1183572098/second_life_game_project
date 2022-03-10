import json
from django.http import HttpResponse
from game.modules import game_manager, game_process
from django.shortcuts import render, redirect
from game.forms import UserForm, UserProfileForm, AnnouncementForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from game.models import Announcement


def index(request):
    context_dict = {'boldmessage': 'test'}
    return render(request, 'game/index.html', context=context_dict)


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
    return HttpResponse(result)

def add_announcement(request):
    if request.method == 'POST':
        announcement_form = AnnouncementForm(request.POST)
        if announcement_form.is_valid():
            announcement = announcement_form.save(commit=False)
            return redirect('game/admin.html')
        else:
            print(announcement_form.errors)
            return HttpResponse("Invalid announcement. ")
    else:
        return render(request, 'game/announcement.html')


def show_announcement(request):
    context_dict = {}
    context_dict['testing'] = 'This is a test since no announcements currently exist.'
    try:
        announcements = Announcement.objects.all()
        context_dict['announcements'] = announcements
    except Announcement.DoesNotExist:
       context_dict['announcements'] = None
    return render(request, 'game/admin.html', context=context_dict)


def user_logout(request):
    logout(request)
    return redirect('/game/index/')


def start_game(request):
    return render(request, 'game/start.html')


def click_shop(request):
    data = json.loads(request.body.decode())
    manager = game_manager.Manager()
    result = manager.open_shop(data)
    return HttpResponse(result)


def purchase_good(request):
    data = json.loads(request.body.decode())
    manager = game_manager.Manager()
    result = manager.purchase(data)
    return HttpResponse(result)


def use_good(request):
    data = json.loads(request.body.decode())
    manager = game_manager.Manager()
    result = manager.use_good(data)
    return HttpResponse(result)


def choose_option(request):
    data = json.loads(request.body.decode())
    manager = game_manager.Manager()
    result = manager.choose_option(data)
    return HttpResponse(result)


def test(request):
    new_game = game_manager.Manager()
    return HttpResponse(200)

