import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from game.modules import game_manager, game_process
from django.shortcuts import render, redirect
from game.forms import UserForm, UserProfileForm, AnnouncementForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from game.models import Announcement
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    context_dict = {'boldmessage': 'test'}
    return render(request, 'game/index.html', context=context_dict)


def initial_game(request):
    manager = game_manager.Manager()
    result = manager.initial_game(request, game_process.Process())
    print("result: " + str(result))
    return render(request, 'game/initialization.html', context=result)


@csrf_exempt
def random_attribute(request):
    manager = game_manager.Manager()
    result = manager.random_attribute(request)
    print("result: " + str(result))
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def game_confirm(request):
    manager = game_manager.Manager()
    result = manager.start_game(request)
    print("result: " + str(result))
    return HttpResponse(result)


@staff_member_required()
def add_announcement(request):
    announcement_form = AnnouncementForm()
    if request.method == 'POST':
        announcement_form = AnnouncementForm(request.POST)
        if announcement_form.is_valid():
            announcement = announcement_form.save(commit=False)
            return redirect('/game/index/')
        else:
            print(announcement_form.errors)
    return render(request, 'game/announcement.html', {'form':announcement_form})


def show_announcement(request):
    context_dict = {'testing': 'This is a test since no announcements currently exist.'}
    try:
        announcements = Announcement.objects.all()
        context_dict['announcements'] = announcements
    except Announcement.DoesNotExist:
        context_dict['announcements'] = None
    return render(request, 'game/admin.html', context=context_dict)


@login_required()
def user_logout(request):
    logout(request)
    return redirect('/game/index/')


def start_game(request):
    return render(request, 'game/start.html')


def archive(request):
    manage = game_manager.Manager()
    manage.serialize(request)


@csrf_exempt
def click_shop(request):
    manager = game_manager.Manager()
    result = manager.open_shop(request)
    print("result: " + str(result))
    return HttpResponse(result)


@csrf_exempt
def purchase_good(request):
    manager = game_manager.Manager()
    result = manager.purchase(request)
    print("result: " + str(result))
    return HttpResponse(result)


@csrf_exempt
def use_good(request):
    manager = game_manager.Manager()
    result = manager.use_good(request)
    print("result: " + str(result))
    return HttpResponse(result)


@csrf_exempt
def choose_option(request):
    manager = game_manager.Manager()
    result = manager.choose_option(request)
    print("result: " + str(result))
    return HttpResponse(result)


def test(request):
    new_game = game_manager.Manager()
    return HttpResponse(200)


def game(request):
    return render(request, 'game/game.html')
