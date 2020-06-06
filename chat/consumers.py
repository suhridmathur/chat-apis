import asyncio
import json

from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from messages.service import get_user_from_token, get_user_from_id, get_thread, save_message
from messages.models import ChatMessage, Thread

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        token = (self.scope.get('query_string').decode('utf-8')).split('=')[1]
        this_user = get_user_from_token(token)
        other_user = get_user_from_id(self.scope['url_route']['kwargs']['user_id'])
        thread = get_thread(this_user, other_user)
        chat_room = f"thread_{thread.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            "type":"websocket.accept",
        })

    async def websocket_receive(self, event):
        print("received", event)
        message_dict = json.loads(event.get('text'))
        message = message_dict.get('message')
        sender = get_user_from_token(message_dict.get('token'))
        user_id = self.scope['url_route']['kwargs']['user_id']
        receiver = get_user_from_id(user_id)
        print("Receiver", receiver)
        
        save_message(sender, receiver, message)
        response = {
            "message" : message,
            "username": sender.username
        }
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "chat_message",
                "text": json.dumps(response)
            }            
        )
    
    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)
