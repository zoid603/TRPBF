from django.urls import path

from . import views

app_name = 'achievement'

urlpatterns = [
    path('', views.achievements, name='list'),
    path(
        '<int:achievement_id>/',
        views.achievement_detail,
        name='detail',
    ),
]
