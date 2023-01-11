# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Community, CommunityChat
from accounts.models import CustomUser
from channels.db import database_sync_to_async
from django.core import serializers


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def load_massage(self, room_name):
        messages = CommunityChat.objects.get(community_name=room_name)

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_massage(self, user_id, community_id, whats_in, content):
        community = Community.objects.get(id=community_id)
        user = CustomUser.objects.get(user_id=user_id)
        CommunityChat.objects.create(user=user, community=community, whats_in=whats_in, content=content)

    @database_sync_to_async
    def load_users(self, user_id):
        user = CustomUser.objects.get(user_id=user_id)
        u = {}
        u["user_id"] = user_id
        u["username"] = user.username
        u["profile_image"] = user.profile_image

    @database_sync_to_async
    def get_user(self, user_id):
        user = CustomUser.objects.get(user_id=user_id)
        return user


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_id = text_data_json['user_id']
        user = await self.get_user(user_id)
        user_image = str(user.profile_image)
        username = user.username

        whats_in = text_data_json['whats_in']
        message = text_data_json['message']
        time = text_data_json['time']

        if whats_in == 'chat':
            await self.save_massage(user_id, self.room_id, whats_in, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user_id': user_id,
                'user_image': user_image,
                'username': username,
                'whats_in': whats_in,
                'message': message,
                'time': time,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        user_image = event['user_image']
        username = event['username']
        whats_in = event['whats_in']
        time = event['time']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user_id':user_id,
            'user_image':user_image,
            'username':username,
            'whats_in': whats_in,
            'message': message,
            'time':time,
        }))