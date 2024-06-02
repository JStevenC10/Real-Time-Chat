import json
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from .models import Message, Room

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        self.room_group_name = 'chat_{}'.format(self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name        
        )
        await self.accept()
    

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data_to_json = json.loads(text_data)  

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": data_to_json["message"],
                "username": data_to_json["username"],
                "room": data_to_json["room"]
            }
        )
    
        await self.save_message(message=data_to_json["message"], username=data_to_json["username"],
                               room=data_to_json["room"])    
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "room": event["room"]
        }))
    
    @database_sync_to_async
    def save_message(self, message, username, room):
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room)
        Message.objects.create(room=room, user=user, body=message)