import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, PrivateMessage
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from myaccount.models import Account

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if isinstance(self.user, AnonymousUser):
            await self.close()
        else:
            self.room_group_name = f'user_{self.user.username}'
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        if not isinstance(self.user, AnonymousUser):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        issuer_username = text_data_json['issuer']
        receiver_username = text_data_json['receiver']

        if isinstance(self.user, AnonymousUser):
            return
        
        issuer = await database_sync_to_async(Account.objects.get)(username=issuer_username)
        receiver = await database_sync_to_async(Account.objects.get)(username=receiver_username)

        conversation, created = await database_sync_to_async(Conversation.objects.get_or_create)(
            user1=issuer,
            user2=receiver
        )

        private_message = await database_sync_to_async(PrivateMessage.objects.create)(
            conversation=conversation,
            message=message,
            issuer=issuer,
            receiver=receiver
        )

        await self.channel_layer.group_send(
            f'user_{receiver_username}',
            {
                'type': 'chat_message',
                'message': message,
                'issuer': issuer_username,
                'receiver': receiver_username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        issuer = event['issuer']
        receiver = event['receiver']

        await self.send(text_data=json.dumps({
            'message': message,
            'issuer': issuer,
            'receiver': receiver
        }))
