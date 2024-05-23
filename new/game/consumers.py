import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ball, pad

class PongConsumer(AsyncWebsocketConsumer):

    players = {}
    async def connect(self):
        self.game_task = None
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'pong_{self.room_name}'
        self.player_number = None
        print("YO!")
        self.ball = ball(400, 300, 10)
        #self.ball_position = [50, 50]
        #self.ball_velocity = [1, 1]
        #self.paddle1_position = 50
        #self.paddle2_position = 50
        self.testG = pad(0, 260, 10, 80, ball, 2, None)
        self.testD = pad(790, 260, 10, 80, ball, 2, self.testG)
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
                direction = data.get('direction')
                #print(direction)
                player = PongConsumer.players[self.channel_name]['player_number']
                if player == 'left':
                    if direction == -1:
                        self.testG.move(False)    
                    if direction == 1:
                        self.testG.move(True)
                elif player == 'right':
                    if direction == -1:
                        self.testD.move(False)
                    elif direction == 1:
                        self.testD.move(True)

    
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
            #self.update_ball_position()
            self.ball.move()
            self.update_ball_position()
            self.collisions(self.ball, self.testG, self.testD)
            await self.send_game_state()
            await asyncio.sleep(0.05)

    def collisions(self ,ball, leftPad, rightPad):
        #print("2222")
        #self.ball.x += self.ball.xSpeed
        #self.ball.y += self.ball.ySpeed

        if (ball.y + ball.rad >= 600) or (ball.y - ball.rad <= 0) :
            ball.ySpeed *= -1
        if ball.xSpeed < 0 :
            if ball.y >= leftPad.y and ball.y <= leftPad.y + (leftPad.height / 2):
                if ball.x - ball.rad <= leftPad.x + leftPad.width :
                    ball.xSpeed *= -1
                    if ball.xSpeed < 8.1 :
                        ball.xSpeed += 0.05
                    print(ball.xSpeed)
                    midPad = leftPad.y + leftPad.height / 2
                    diff = midPad - ball.y
                    reduc = (leftPad.height / 2) / ball.maxSpeed
                    ball.ySpeed = diff / reduc
        elif ball.xSpeed > 0 :
            #print("333")
            print(ball.y, rightPad.y)
            if ball.y >= rightPad.y and ball.y <= rightPad.y + rightPad.height:
                #print("4")
                if ball.x + ball.rad >= rightPad.x :
                    #print("5")
                    ball.xSpeed *= -1
                    if ball.xSpeed > -8.1 :
                        ball.xSpeed += -0.05
                    #print(ball.xSpeed)
                    midPad = rightPad.y + rightPad.height / 2
                    diff = midPad - ball.y
                    reduc = (leftPad.height / 2) / ball.maxSpeed
                    ball.ySpeed = diff / reduc

    def update_ball_position(self):
        #self.ball.x += self.ball.xSpeed
        #self.ball.y += self.ball.ySpeed
        #if self.ball.y <= 0 or self.ball.y >= 600:
            #self.ball.ySpeed = -self.ball.ySpeed
        if self.ball.x <= 0:
            #if abs(self.ball.y - self.testG.y) < 10:
                #self.ball.xSpeed = -self.ball.xSpeed
            #else:
                #print("BUUUUUUUT")
                self.score[1] += 1
                self.reset_all()
        if self.ball.x >= 800:
            #if abs(self.ball.y - self.testD.y) < 10:
                #self.ball.xSpeed = -self.ball.xSpeed
            #else:
            #print("BUUUUUUUT")
            self.score[0] += 1
            self.reset_all()

    def reset_all(self):
        #self.ball.x, ball.y = [400, 300]
        #self.ball.xSpeed, ball.ySpeed = [0, 0]
        self.ball.reset()
        self.testD.y = 260
        self.testG.y = 260


    async def send_game_state(self):
        game_state = {
            'ball_position': [self.ball.x, self.ball.y],
            'paddle1_position': (self.testG.y),
            'paddle2_position': (self.testD.y),
            'score': self.score,
        }
        #print(game_state)
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

