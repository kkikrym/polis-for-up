# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<room_id>[A-Za-z0-9_-]+)', consumers.ChatConsumer.as_asgi()),
]
