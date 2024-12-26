import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Lazy import models to avoid early settings access
        from .models import Conversation
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"conversation_{self.conversation_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        from .models import Message, Conversation
        data = json.loads(text_data)
        conversation = await sync_to_async(Conversation.objects.get)(id=self.conversation_id)
        message = await sync_to_async(Message.objects.create)(
            conversation=conversation,
            sender=self.scope['user'],
            content=data['message']
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data['message'],
                'sender': self.scope['user'].username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))
