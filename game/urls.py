from django.urls import path
from game import views
from django.views import View

app_name = 'second_life'

urlpatterns = [
    path('index/', views.index, name='index'),
   #path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('initial/', views.initial_game, name='initial'),
    path('initial/random/', views.random_attribute, name='random'),
    path('initial/confirm/', views.game_confirm, name='confirm'),
    path('archive/', views.archive, name='archive'),
    path('shop/', views.click_shop, name='shop'),
    path('purchase/', views.purchase_good, name='purchase'),
    path('use/', views.use_good, name='use'),
    path('game/', views.reload, name='game'),
    path('option/', views.choose_option, name='choose_option'),
    path('post/', views.add_announcement, name='add_announcement'),
    path('announcements/', views.show_announcement, name='show_announcement'),
    path('next/', views.next_year, name='next_year'),
    path('archive/read/', views.load_game, name='load_game'),
    path('archive/save/', views.save_game, name='save_game'),
    path('start/', views.start, name='start')
]
