from django.urls import path

from . import views

app_name = 'progress_records'

urlpatterns = [
    path('', views.progress_list, name='list'),
    path(
        '<int:progress_id>/',
        views.progress_detail,
        name='detail',
    ),
]
