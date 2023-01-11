# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Team, TeamChat, TeamThread
from accounts.models import CustomUser
from channels.db import database_sync_to_async
from django.core import serializers

NOTIFICATION_FORMAT = {
    "top":{},

    "community":{},

    "team":{
        "threads":{},
    },

}

class ChatConsumer(AsyncWebsocketConsumer):

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
    def save_massage(self, user_id, thread_id, whats_in, content):
        thread=TeamThread.objects.get(id=thread_id)
        chat = TeamChat.objects.create(user_id=user_id, thread=thread, whats_in=whats_in, content=content)
        #chat.seen.add(CustomUser.objects.get(user_id=user_id))
        users = thread.team.users.all()
        for u in users:
            n = u.notifications
            if n == None:
                n = NOTIFICATION_FORMAT
                n["team"]["threads"][thread_id] = 1
            else:
                if not n["team"]["threads"].get(thread_id):
                    n["team"]["threads"][thread_id] = 1
                else:
                    n["team"]["threads"][thread_id] += 1
            u.notifications = n
            u.save()
        chat.save()

    @database_sync_to_async
    def reset_notifications(self, user_id, thread_id):
        u = CustomUser.objects.get(user_id=user_id)
        n = u.notifications
        if n == None:
            n = NOTIFICATION_FORMAT
            n["team"]["threads"][thread_id] = 0
        else:
            n["team"]["threads"][thread_id] = 0
        u.notifications = n
        u.save()


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

        if whats_in == 'join_announce':
            await self.reset_notifications(user_id, self.room_id)

        elif whats_in == 'exit_announce':
            await self.reset_notifications(user_id, self.room_id)

        else:
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
                    'group_name': self.room_group_name,
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
            'type': 'chat_message',
            'user_id':user_id,
            'user_image':user_image,
            'username':username,
            'whats_in': whats_in,
            'message': message,
            'time':time,
        }))