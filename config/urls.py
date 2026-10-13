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
