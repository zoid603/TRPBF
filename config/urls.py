from django.conf import settings
from django.contrib import admin
from django.urls import include, path

handler404 = "homepage.views.page_not_found"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('games/', include('games_app.urls')),
    path('achievements/', include('achievement.urls')),
    path('progress/', include('progress_records.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

admin.site.site_header = "Game Achievement Tracker"
admin.site.site_title = "Каталог достижений"
admin.site.index_title = "Данные каталога"
