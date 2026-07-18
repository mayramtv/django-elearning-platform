# The provenance of the following code is from:  
    # University of London Advance Web Development module
    # Lectures and Labs presented by Dr Daniel Buchan


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # subscribe to a uncomming user on redis stack
        self.room_name = self.scope['url_route']['kwargs']['name']
        # group of users name
        self.room_group_name = 'chat_%s' % self.room_name

        # subscribe incoming user to channel in redis
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)  # specify json  data
        chat = text_data_json['chat']     # get message 
        print('====', self.room_name, chat)

        # save to DB
        await self.save_chat(self.name, 
                                chat)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': chat,
            }
        )

    async def chat_message(self, event):
        chat = event['message']

        await self.send(text_data=json.dumps({        # send data back to users
            'message': chat
        }))

    @sync_to_async
    def create_chat(self, room_name, chat):
        Chat.objects.create(chatroom=Chatroom.objects.get(name=room_name), content=chat)

    async def save_save_chatmessage(self, room_name, chat):
        # print('====++', room_name, message)
        await self.create_chat(room_name, chat)