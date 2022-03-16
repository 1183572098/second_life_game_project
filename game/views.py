import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from game.modules import game_manager, game_process, archive_module
from django.shortcuts import render, redirect
from game.forms import UserForm, UserProfileForm, AnnouncementForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from game.models import Announcement, Record
from django.contrib.admin.views.decorators import staff_member_required
import pickle


def index(request):
    context_dict = {'boldmessage': 'test'}
    return render(request, 'game/index.html', context=context_dict)

@login_required
@csrf_exempt
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
    return HttpResponse(json.dumps(result), content_type='application/json')


def add_announcement(request):
    announcement_form = AnnouncementForm()
    if request.method == 'POST':
        announcement_form = AnnouncementForm(request.POST)
        if announcement_form.is_valid():
            announcement_form.save(commit=True)
            return redirect('second_life:index')
        else:
            print(announcement_form.errors)
    return render(request, 'game/announcement.html', {'form': announcement_form})


def show_announcement(request):
    context_dict = {'testing': 'This is a test since no announcements currently exist.'}
    try:
        announcements = Announcement.objects.all()
        context_dict['announcements'] = announcements
    except Announcement.DoesNotExist:
        context_dict['announcements'] = None
    return render(request, 'game/admin.html', context=context_dict)


@login_required
def archive(request):
    user_id = request.user.id
    context_dict = {'testing': 'This is a test since no announcements currently exist.'}
    try:
        archives = Record.objects.get(user_id=user_id)
        context_dict['archives'] = archives
    except Record.DoesNotExist:
        context_dict['archives'] = None
    result = archive_module.enter_archive(request)
    return render(request, 'game/readArchive.html', context=result)
    # return render(request, 'game/saveArchive.html')


def readArchive(request):
    return render(request, 'game/readArchive.html')


def saveArchive(request):
    return render(request, 'game/saveArchive.html')


def save_game(request):
    if request.method == 'POST':
        manage = game_manager.Manager()
        manage.serialize(request)
        return render(request, 'game/saveArchive.html')
    else:
        return render(request, 'game/index.html')


def load_game(request):
    context_dict = {'testing': 'This is a test since no announcements currently exist.'}
    if request.method == 'GET':
        user_id = request.user.id
        loc = request.GET.get('location')
        archive = Record.objects.get(user_id=user_id, location=loc)
        archive_data = pickle.load(archive['data'])
        return render(request, 'game/game.html')
    else:
        return render(request, 'game/index.html')


@csrf_exempt
def click_shop(request):
    manager = game_manager.Manager()
    result = manager.open_shop(request)
    print("result: " + str(result))
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def purchase_good(request):
    manager = game_manager.Manager()
    result = manager.purchase(request)
    print("result: " + str(result))
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def use_good(request):
    manager = game_manager.Manager()
    result = manager.use_good(request)
    print("result: " + str(result))
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def choose_option(request):
    manager = game_manager.Manager()
    result = manager.choose_option(request)
    print("result: " + str(result))
    return HttpResponse(json.dumps(result), content_type='application/json')


def game(request):
    manager = game_manager.Manager()
    result = manager.enter_game(request)
    print("result: " + str(result))
    if result is None:
        return redirect('second_life:index')
    result["user_id"] = request.user.id
    return render(request, 'game/game.html', context=result)


def initialization(request):
    context_dict = {}
    user_id = request.user.id
    context_dict["user_id"] = user_id
    return render(request, 'game/initialization.html', context=context_dict)


@csrf_exempt
def next_year(request):
    manager = game_manager.Manager()
    result = manager.enter_game(request)
    print("result: " + str(result))
    return HttpResponse(json.dumps(result), content_type='application/json')
