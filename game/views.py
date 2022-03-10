import json
from django.http import HttpResponse
from game.modules import game_manager, game_process
from django.shortcuts import render, redirect
from game.forms import UserForm, UserProfileForm, AnnouncementForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from game.modules import login_system
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


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'game/register.html', context={'user_form': user_form, 'profile_form': profile_form,
                                                          'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('/game/index/')
            else:
                return HttpResponse("Your SecondLife account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'game/login.html')


def add_announcement(request):
    if request.method == 'POST':
        announcement_form = AnnouncementForm(request.POST)
        if announcement_form.is_valid():
            announcement = announcement_form.save(commit=False)
            return redirect('admin.html')
        else:
            print(announcement_form.errors)
            return HttpResponse("Invalid announcement. ")
    else:
        return render(request, 'announcement.html')


def show_announcement(request):
    context_dict = {}
    try:
        announcements = Announcement.objects.all()
        context_dict['announcements'] = announcements
    except Announcement.DoesNotExist:
        context_dict['announcements'] = None
    return render(request, 'admin.html', context=announcements)


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

