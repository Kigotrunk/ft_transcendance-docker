from .globals import queue, matchmaking_task, removeGame, removeCup, removePlayer, players, games, cups, nb_room, setPlayer, setGame, setCups, getPlayer, getGame, getCup
import json
import time
import asyncio
from .pongGame import pongGame, matchmaking
from .tournament import tournament
from channels.db import database_sync_to_async
from myaccount.models import Account

class Player:
    def __init__(self, id, name, elo, consumers):
        self.id = id
        self.name = name
        self.elo = elo
        self.consumers = consumers

        self.room_name = None
        self.room = None
        self.cup_name = None
        self.cup = None
        self.room_group_name = None
        self.player_side = None
        self.in_lobby = False
        self.in_cup = False
        self.in_queue_cup = False
        self.in_queue = False

    async def disconnect(self):
        if self.in_queue_cup == True :
            await self.cup.leavingPlayer(self)
        if self.in_lobby == True :
            if self.room.left_player == self:
                self.room.score[1] = 5
                self.room.game_over = True
            elif self.room.right_player == self:
                self.room.score[0] = 5
                self.room.game_over = True
        
        for player in queue:
            if self == player:
                queue.remove(self)
        
        global matchmaking_task
        if not queue and matchmaking_task and not matchmaking_task.done():
            matchmaking_task.cancel()
            matchmaking_task = None

        await self.force_save()

    async def force_save(self):
        user = await database_sync_to_async(Account.objects.get)(id=self.id)
        user.is_connected = False
        await database_sync_to_async(user.save)()

    def move(self, direction):
        if self.room.game_state:
            print("Moving")
            if self.player_side == 'left':
                print("left")
                self.room.leftPad.direction = direction
            elif self.player_side == 'right':
                self.room.rightPad.direction = direction

    async def join_private_game(self, room_name):
        self.room_name = room_name
        self.in_lobby = False
        self.room = getGame(self.room_name)
        self.room_group_name = f"game_{self.room_name}"
        if self.room is None:
            await self.create_room()
            print(f"Creating room {self.room_name}")
        else:
            await self.join_existing_room()
            print(f"Joining room {self.room_name}")

    async def join_queue(self):
        if self in queue:
            return
        print('Adding player to queue...')
        self.wait_time = time.time()
        queue.append(self)
        self.in_queue = True
        print (f"{self.name} added to queue")
        global matchmaking_task
        if matchmaking_task is None or matchmaking_task.done():
            matchmaking_task = asyncio.create_task(matchmaking(queue))
            print('Matchmaking task created')

    async def leave_queue(self):
        global matchmaking_task
        global queue
        if self in queue:
            queue.remove(self)
            if not queue and matchmaking_task and not matchmaking_task.done():
                matchmaking_task.cancel()
                matchmaking_task = None
            self.in_queue = False
            print(f"{self.name} removed from queue")
        
    async def join_match(self):
        self.room_name = f"{nb_room}room"
        self.room = getGame(f"{nb_room}room")
        self.room_group_name = f"game_{self.room_name}"
        
        if self.room is None :
            print(f"Creating room {self.room_name}")
            await self.create_room()
        else:
            print(f"Joining room {self.room_name}")
            await self.join_existing_room()
        self.in_queue = False

    async def create_room(self):
        await self.consumers.channel_layer.group_add(
            self.room_group_name,
            self.consumers.channel_name
        )
        self.player_side = 'left'
        self.room = pongGame(self.room_name, self.consumers)
        setGame(self.room_name, self.room)
        self.room.left_player = self
        #self.in_lobby = True

    async def join_existing_room(self):
        if self.room.left_player == self:
            return
        if self.room.player_number == 1:
            await self.consumers.channel_layer.group_add(
                self.room_group_name,
                self.consumers.channel_name
            )
            self.player_side = 'right'
            self.room.right_player = self
            await self.room.launchGame("Online", 0, False, self.consumers)
            #self.in_lobby = True

    async def join_cup(self):
        i = 0
        while not self.in_queue_cup:
            self.cup_name = f"{i}cup"
            self.cup = getCup(self.cup_name)
            self.cup_group_name = f"game_{self.cup_name}"
            if self.cup is None:
                await self.create_cup(i)
            else:
                if self.cup.player_count < 8:
                    await self.join_existing_cup()
            i += 1
        
    async def leave_cup(self):
        if self.in_queue_cup == True:
            await self.consumers.channel_layer.group_discard(
                self.cup_group_name,
                self.consumers.channel_name
            )
            await self.cup.leavingPlayer(self)
            self.cup = None
            self.cup_group_name = None
        self.in_queue_cup = False

    async def create_cup(self, i=None):
        self.in_queue_cup = True
        await self.consumers.channel_layer.group_add(
            self.cup_group_name,
            self.consumers.channel_name
        )
        self.cup = tournament(self, self.cup_name)
        setCups(self.cup_name, self.cup)
        await self.cup.sendLobbyState()

    async def join_existing_cup(self):
        self.in_queue_cup = True
        await self.consumers.channel_layer.group_add(
            self.cup_group_name,
            self.consumers.channel_name
        )
        await self.cup.newContestant(self)

    async def setup_ai_game(self, diff):
        self.diff = diff
        self.room_name = "ai"
        i = 0
        while getGame(self.room_name) is not None:
            self.room_name = f"{i}ai"
            i += 1
        self.room_group_name = f"game_{self.room_name}"
        await self.consumers.channel_layer.group_add(
            self.room_group_name,
            self.consumers.channel_name
        )
        self.player_side = 'left'
        self.room = pongGame(self.room_name, self.consumers)
        setGame(self.room_name, self.room)
        self.room.left_player = self
        await self.room.launchGame("LM", self.diff, False, None)
    
    async def lost_cup(self):
        await self.consumers.channel_layer.group_discard(
            self.cup_group_name,
            self.consumers.channel_name
        )
        self.cup_group_name = None
        self.cup = None
        self.in_cup = False
