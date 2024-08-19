import json
import time
import asyncio
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ball, pad, partie 
from .globals import setGame, getGame, removeGame, setCups, getCup, removeCup, setPlayer, getPlayer, removePlayer, queue, nb_room, players, games, cups, matchmaking_task
from .pongGame import pongGame, matchmaking
from channels.db import database_sync_to_async
from .tournament import tournament
from myaccount.models import Account
from .player import Player

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if isinstance(self.user, AnonymousUser):
            await self.close()
        self.player = getPlayer(self.user.id)
        if self.player != None:
            await self.close()
            return
        self.player = Player(self.user.id, self.user.username, self.user.elo, self)
        setPlayer(self.user.id, self.player)
        await self.accept()
        self.user.is_connected = True
        await database_sync_to_async(self.user.save)()

    async def disconnect(self, close_code):
        if self != self.player.consumers:
            return
        await self.player.disconnect()
        removePlayer(self.user.id)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)

    async def game_info(self, event):
        game_info = event['game_info']
        await self.send(text_data=json.dumps(game_info))

    async def lobby_state(self, event):
        lobby_state = event['lobby_state']
        await self.send(text_data=json.dumps(lobby_state))

    async def next_game_countdown(self, event):
        next_game_countdown = event['next_game_countdown']
        await self.send(text_data=json.dumps(next_game_countdown))

    async def cup_match_result(self, event):
        cup_match_result = event['cup_match_result']
        await self.send(text_data=json.dumps(cup_match_result))

    async def game_state(self, event):
        game_state = event['game_state']
        await self.send(text_data=json.dumps(game_state))
        
    async def tournament_state(self, event):
        tournament_state = event['tournament_state']
        await self.send(text_data=json.dumps(tournament_state))

    async def next_match(self, event):
        next_match = event['next_match']
        await self.send(text_data=json.dumps(next_match))

    async def countdown(self, event):
        countdown = event['countdown']
        await self.send(text_data=json.dumps({'type': 'countdown', 'countdown': countdown}))

    async def game_result(self, event):
        game_result = event['game_result']
        await self.send(text_data=json.dumps({'type': 'game_result', 'game_result': game_result}))
