import json
from django.http import HttpResponse
from game.modules import game_manager, game_process
from django.shortcuts import render, redirect
from game.forms import UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
    
    return render(request, 'game/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


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


def test(request):
    new_game = game_manager.Manager()
    return HttpResponse(200)
