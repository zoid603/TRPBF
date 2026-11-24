from django.urls import path

from . import views

app_name = 'games_app'

urlpatterns = [
    path('', views.games, name='list'),
    path('<int:game_id>/', views.game_detail_by_id, name='detail_by_id'),
    path('<slug:game_slug>/', views.game_detail, name='detail'),
]
