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
    manager = game_manager.Manager()
    manager.exit_game(request)
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


@login_required
def add_announcement(request):
    user = request.user
    if user.is_staff:
        announcement_form = AnnouncementForm()
        if request.method == 'POST':
            announcement_form = AnnouncementForm(request.POST)
            if announcement_form.is_valid():
                announcement_form.save(commit=True)
                return redirect('second_life:index')
            else:
                print(announcement_form.errors)
        return render(request, 'game/announcement.html', {'form': announcement_form})
    else:
        return render(request, 'game/login.html')


def show_announcement(request):
    context_dict = {}
    try:
        announcements = Announcement.objects.all()
        context_dict['announcements'] = announcements
    except Announcement.DoesNotExist:
        context_dict['announcements'] = None
    return render(request, 'game/admin.html', context=context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            if 'player' in request.POST:
                user.is_staff = False
            if 'administrator' in request.POST:
                user.is_staff = True
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'game/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('second_life:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'game/login.html')


@login_required
def archive(request):
    result = archive_module.enter_archive(request)
    print("result:" + str(result))
    return render(request, 'game/archive.html', context=result)


@csrf_exempt
def save_game(request):
    if request.method == 'POST':
        manage = game_manager.Manager()
        result = manage.serialize(request)
        if result.get("success") == 1:
            result.update(archive_module.enter_archive(request))
        print("result: " + str(result))
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render(request, 'game/index.html')


@csrf_exempt
def load_game(request):
    if request.method == 'POST':
        manager = game_manager.Manager()
        result = manager.deserialize(request)
        print("result: " + str(result))
        return HttpResponse(json.dumps(result), content_type='application/json')
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
    return render(request, 'game/game.html', context=result)


@csrf_exempt
def next_year(request):
    manager = game_manager.Manager()
    result = manager.enter_game(request)
    print("result: " + str(result))
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def start(request):
    manager = game_manager.Manager()
    manager.enter_game(request)
    result = manager.reload_game(request)
    print("result: " + str(result))
    if result is None:
        return redirect('second_life:index')
    return render(request, 'game/game.html', context=result)


@csrf_exempt
def reload(request):
    manager = game_manager.Manager()
    result = manager.reload_game(request)
    print("result: " + str(result))
    if result is None:
        return redirect('second_life:index')
    elif result["success"] == 0:
        return redirect('second_life:initial')
    elif len(result["event_id"]) == 0:
        return redirect('second_life:initial')
    return render(request, 'game/game.html', context=result)
