from django.urls import path
from game import views
from django.views import View

app_name = 'second_life'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('initial/', views.initial_game, name='initial'),
    path('initial/random/', views.random_attribute, name='random'),
    path('initial/confirm/', views.game_confirm, name='confirm'),
    path('start/', views.start_game, name='start_game'),
    path('shop/', views.click_shop, name='shop'),
    path('purchase/', views.purchase_good, name='purchase'),
    path('use/', views.use_good, name='use'),
    path('game/', views.game, name='game'),
    path('option/', views.choose_option, name='choose_option'),
    path('post/', views.add_announcement, name='add_announcement'),
    path('announcements/', views.show_announcement, name='show_announcement'),
]