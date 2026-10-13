from django.urls import path

from . import views

urlpatterns = [
    path('', views.achievements, name='achievements'),
    path(
        '<int:achievement_id>/',
        views.achievement_detail,
        name='achievement_detail',
    ),
]
