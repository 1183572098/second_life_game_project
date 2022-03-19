import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'second_life_game_project.settings')

import django
django.setup()
from game.models import Announcement
from django.contrib.auth.models import User


def populate():
    announcements = [
        {
            'title': 'Our Game is Officially Launched!',
            'content': 'Our game officially launched on March 18th! Welcome to play!',
        },
        {
            'title': 'Update Announcement',
            'content': '''Dear players, we will preview a 3-hour stop-service update on March 22nd, 
                            when the player will not be able to log in to the game.''',
        },
        {
            'title': 'Value adjustment',
            'content': '''Dear players, we will adjust the game value on March 26th to adjust the game value, 
                            and the properties of some events will change.''',
        }
    ]

    users = [
        {
            'username': 'player1',
            'password': 'player1',
            'is_staff': False,
        },
        {
            'username': 'player2',
            'password': 'player2',
            'is_staff': False,
        },
        {
            'username': 'administrator',
            'password': 'administrator',
            'is_staff': True,
        }
    ]

    for announcement in announcements:
        add_announcement(announcement)

    for user in users:
        add_user(user)


def add_user(user):
    u = User.objects.get_or_create(username=user['username'])[0]
    u.set_password(user['password'])
    u.is_staff = user['is_staff']
    u.save()
    return u


def add_announcement(announcement):
    a = Announcement.objects.get_or_create(title=announcement['title'])[0]
    a.content = announcement['content']
    a.save()
    return a


if __name__ == '__main__':
    print('Starting Game population script...')
    populate()
