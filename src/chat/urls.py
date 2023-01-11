# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.TeamView.as_view(), name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)