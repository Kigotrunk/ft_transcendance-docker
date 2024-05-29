import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, PrivateMessage
from myaccount.models import Account
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "notifications",
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "notifications",
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_json = json.loads(text_data)
        message = text_json['message']
        await self.channel_layer.group_send



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.room_name}'
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
        data = json.loads(text_data)
        message = data['message']
        issuer_id = data['issuer']
        room_name = self.room_name

        conversation = await sync_to_async(Conversation.objects.get)(id=room_name)
        issuer = await sync_to_async(Account.objects.get)(id=issuer_id)
        receiver = await sync_to_async(lambda: conversation.user1 if conversation.user2 == issuer else conversation.user2)()

        private_message = await sync_to_async(PrivateMessage.objects.create)(
            conversation=conversation,
            message=message,
            issuer=issuer,
            receiver=receiver
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'issuer': issuer_id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        issuer = event['issuer']
        await self.send(text_data=json.dumps({
            'message': message,
            'issuer': issuer
        }))


    @database_sync_to_async
    def get_user(self, user_id):
        return Account.objects.get(id=user_id)

    @database_sync_to_async
    def get_conversation(self, chat_id):
        return Conversation.objects.get(id=chat_id)

    @database_sync_to_async
    def save_message(self, conversation, issuer, message):
        PrivateMessage.objects.create(conversation=conversation, issuer=issuer, message=message)
