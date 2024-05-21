import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class PongConsumer(AsyncWebsocketConsumer):

    players = {}
    async def connect(self):
        self.game_task = None
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'pong_{self.room_name}'

        self.player_number = None
        self.ball_position = [50, 50]
        self.ball_velocity = [1, 1]
        self.paddle1_position = 50
        self.paddle2_position = 50
        self.score = [0, 0]

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        PongConsumer.players[self.channel_name] = {
            'player_number': None,
            'room_name': self.room_name
        }

    async def disconnect(self, close_code):
        # print("disconnect !")
        if self.channel_name in PongConsumer.players:
            del PongConsumer.players[self.channel_name]
        
        players_count = sum(1 for player in PongConsumer.players.values() if player['room_name'] == self.room_name)
        
        if players_count < 2:
            self.game_task.cancel()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # print(text_data)

        if 'action' in data:
            action = data['action']

            if action == 'join':
                # Récupérer le nombre de joueurs dans ce salon
                players_count = sum(1 for player in PongConsumer.players.values() if player['room_name'] == self.room_name)
                
                if players_count == 1:
                    self.player_number = 'left'

                elif players_count == 2:
                    self.player_number = 'right'

                elif players_count > 2:
                    self.player_number = 'spectator'

                PongConsumer.players[self.channel_name] = {
                    'player_number': self.player_number,
                    'room_name': self.room_name
                }

                await self.send(json.dumps({'player': self.player_number}))
                if players_count == 2:
                    asyncio.create_task(self.start_countdown())

                # Mettre à jour l'affichage de l'état lorsqu'un joueur se connecte
                if players_count == 2:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'game_state',
                            'game_state': {
                                'waiting': False
                            }
                        }
                    )
            elif action == 'move':
                if data['player'] == 'left':
                    self.paddle1_position = min(max(self.paddle1_position + data['delta'], 0), 100)
                elif data['player'] == 'right':
                    self.paddle2_position = min(max(self.paddle2_position + data['delta'], 0), 100)


    async def start_countdown(self):
        for i in range(3, 0, -1):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'countdown',
                    'countdown': i
                }
            )
            await asyncio.sleep(1)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'countdown',
                'countdown': "Go!"
            }
        )
        await asyncio.sleep(1)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'countdown',
                'countdown': ""
            }
        )
        self.game_task = asyncio.create_task(self.game_loop())

    async def game_loop(self):
        while True:
            self.update_ball_position()
            await self.send_game_state()
            await asyncio.sleep(0.03)

    def update_ball_position(self):
        self.ball_position[0] += self.ball_velocity[0]
        self.ball_position[1] += self.ball_velocity[1]

        if self.ball_position[1] <= 0 or self.ball_position[1] >= 100:
            self.ball_velocity[1] = -self.ball_velocity[1]

        if self.ball_position[0] <= 0:
            if abs(self.ball_position[1] - self.paddle1_position) < 10:
                self.ball_velocity[0] = -self.ball_velocity[0]
            else:
                self.score[1] += 1
                self.reset_ball()

        if self.ball_position[0] >= 100:
            if abs(self.ball_position[1] - self.paddle2_position) < 10:
                self.ball_velocity[0] = -self.ball_velocity[0]
            else:
                self.score[0] += 1
                self.reset_ball()

    def reset_ball(self):
        self.ball_position = [50, 50]
        self.ball_velocity = [1, 1]

    async def send_game_state(self):
        game_state = {
            'ball_position': self.ball_position,
            'paddle1_position': self.paddle1_position,
            'paddle2_position': self.paddle2_position,
            'score': self.score,
        }
        # print (game_state)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_state',
                'game_state': game_state
            }
        )

    async def game_state(self, event):
        game_state = event['game_state']
        await self.send(text_data=json.dumps(game_state))

    async def countdown(self, event):
        countdown = event['countdown']
        await self.send(text_data=json.dumps({'countdown': countdown}))
