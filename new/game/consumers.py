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
        self.player = Player(self.user.id, self.user.username, self.user.elo, self)
        setPlayer(self.user.id, self.player)
        await self.accept()
        self.user.is_connected = True
        await database_sync_to_async(self.user.save)()

    async def disconnect(self, close_code):
        await self.player.disconnect()
        removePlayer(self.user.id)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        action = data.get('action')
        print(action)
        if action == 'join' : 
            if self.in_queue == False and self.in_queue_cup == False and self.in_cup == False and self.in_lobby == False :
                mode = data.get('mode')
                room_name = data.get('room')
                
                print(mode)
                print(room_name)
                # if mode == 'pvp':
                    # self.in_lobby = False
                        
                    # if room_name[:4] != "room" and room_name != "cup":
                    #     self.room_name = room_name.replace(" ", "")
                    #     if int(self.room_name.split("-")[0]) != self.user.id and int(self.room_name.split("-")[1]) != self.user.id:
                    #         print("Invalid room name")
                    #         return
                    #     self.room = getGame(self.room_name)
                    #     self.room_group_name = f"game_{self.room_name}"
                        
                    #     if self.room is None:
                    #         await self.create_room()
                    #     else:
                    #         await self.join_existing_room()
                    # elif room_name == "cup":
                    #     i = 0
                    #     while not self.in_queue_cup:
                    #         self.cup_name = f"{i}cup"
                    #         self.cup = getCup(self.cup_name)
                    #         self.cup_group_name = f"game_{self.cup_name}"
                    #         if self.cup is None:
                    #             await self.create_cup(i)
                    #         else:
                    #             if self.cup.player_count < 8:
                    #                 await self.join_existing_cup()
                    #         i += 1
                    # else:
                    #     print("Invalid room name")
                        
                # elif mode == 'ai':
                #     await self.setup_ai_game(data.get('room'))
                    
        # elif action == 'move' and self.room and not self.room.game_over:
        #     if self.room.game_state:
        #         direction = data.get('direction')
        #         if self.player_side == 'left':
        #             self.room.leftPad.direction = direction
        #         elif self.player_side == 'right':
        #             self.room.rightPad.direction = direction

        # elif action == 'leave_queue':
        #     player_id = data.get('player_id')
        #     await self.leave_queue()

        # elif action == 'leave_cup':
        #     if self.in_queue_cup == True:
        #         print("YO")
        #         await self.channel_layer.group_discard(
        #             self.cup_group_name,
        #             self.channel_name
        #         )
        #         await self.cup.leavingPlayer(self.user, self)
        #         self.cup = None
        #         self.cup_group_name = None
        #     self.in_queue_cup = False

        # if action == 'update_user':
        #     username = data.get('user')
        #     if self.in_cup == False :
        #          self.user.username = username
        # elif action == 'status':
        #     await self.send(text_data=json.dumps({
        #         'type': 'status',
        #         'in_lobby': self.in_lobby,
        #         'in_cup': self.in_cup,
        #         'matches' : self.cup.all_rounds if self.in_cup != False else None,
        #         'in_queue': self.in_queue,
        #         'in_queue_cup': self.in_queue_cup,
        #     }))
        #     if self.in_lobby and self.room:
        #         await self.send(text_data=json.dumps({
        #             'type': 'game_info',
        #             'left': self.room.left_player.id if self.room.left_player else None,
        #             'right': self.room.right_player.id if self.room.right_player else None,
        #             'left_username': self.room.left_player.username if self.room.left_player else None,
        #             'right_username': self.room.right_player.username if self.room.right_player else None,
        #         }))


    async def game_info(self, event):
        game_info = event['game_info']
        await self.send(text_data=json.dumps(game_info))

    async def lobby_state(self, event):
        lobby_state = event['lobby_state']
        await self.send(text_data=json.dumps(lobby_state))

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
