import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ball, pad
from .globals import setGame, getGame, removeGame
from .pongGame import pongGame

#Disconnect devra pas detruire lors que launch game est lancer.
#Si il n'a pas ete launch_game DETRUIRE la pong game avec Remove(game)
#si Receive Check if Game started !
#DES MUTEX SA MERE A chaque requete (Si 2 joueurs join la meme room vide en meme temps || si 2 joueurs join room avec 1 joueur dedans etc...)


class PongConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        
    
    async def disconnect(self, close_code):

    # print("disconnect !")
        #if self.channel_name in PongConsumer.players:
        #    del PongConsumer.players[self.channel_name]
        
        #players_count = sum(1 for player in PongConsumer.players.values() if player['room_name'] == self.room_name)
        
        #if players_count < 2:
        #    self.game_task.cancel()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        print(text_data)
        
        action = data.get('action')
        if action == 'join':
            mode = data.get('mode')
            if mode == 'pvp':
                self.room_name = 'test'
                self.room = getGame(self.room_name)
                self.room_group_name = f"game_{self.room_name}"
                if self.room == None:
                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )
                    self.player_side = 'left'
                    self.room = pongGame(self.room_name, self)
                    setGame(self.room_name, self.room)
                else :
                    if self.room.player_number == 1:
                        await self.channel_layer.group_add(
                            self.room_group_name,
                            self.channel_name
                        )
                        self.player_side = 'right'
                        await self.room.launchGame()
            elif mode == 'ai':
                #ia room
                pass
        elif action == 'move':
            if self.room and self.room.game_state == True :
                direction = data.get('direction')
                #print(direction)
                #player = PongConsumer.players[self.channel_name]['player_side']
                #player = data.get('player')
                #player = self.side
                if self.player_side == 'left':
                    self.room.leftPad.direction = direction
                elif self.player_side == 'right':
                    self.room.rightPad.direction = direction
                        

    async def game_state(self, event):
        game_state = event['game_state']
        await self.send(text_data=json.dumps(game_state))

    async def countdown(self, event):
        print("COUNTDOWN")
        countdown = event['countdown']
        await self.send(text_data=json.dumps({'countdown': countdown}))


