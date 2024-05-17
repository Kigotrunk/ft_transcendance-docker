import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ball, pad  # Supposons que vous avez un modèle pour stocker l'état du jeu

class player(AsyncWebsocketConsumer):
    
    padWidth = 20 # à redefinir
    padHeight = 100 # à redefinir
    winWidth = 800 # à redefinir
    winHeight = 600 # à redefinir
    
    orb = ball(winWidth // 2, winHeight // 2, 0)
    leftPad = pad(0, 0, padWidth, padHeight, 0, 0)
    rightPad = pad(800, 600, padWidth, padHeight, 0, 0)
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.start_sending_game_state()

    async def disconnect(self, close_code):

        await self.stop_sending_game_state()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']
        
        if message_type == 'z' and self.leftPad.y - self.leftPad.speed:
            self.leftPad.move(up = True)
        if message_type == 's' and self.leftPad.y + self.leftPad.speed + self.leftPad.height <= self.winHeight :
            self.leftPad.move(up = False)
        if message_type == 'UP' and self.rightPad.y - self.rightPad.speed >= 0 :
            self.rightPad.move(up = True)
        if message_type == 'DOWN' and self.rightPad.y + self.rightPad.speed + self.rightPad.height <= self.winHeight :
            self.rightPad.move(up = False)

    async def send_game_state_update(self):

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room',
                'ball_x': self.orb.x,
                'ball_y': self.orb.y,
                'left_pad_y': self.leftPad.y,
                'right_pad_y': self.rightPad.y
            }
        )
    
    def collisions(self, ball, leftPad, rightPad):

        if (ball.y + ball.rad >= self.winHeight) or (ball.y - ball.rad <= 0) :
            ball.ySpeed *= -1
    
        if ball.xSpeed < 0 :
            if ball.y >= leftPad.y and ball.y <= leftPad.y + self.padHeight :
                if ball.x - ball.rad <= leftPad.x + self.padWidth :
                     ball.xSpeed *= -1
                     midPad = leftPad.y + self.padHeight / 2
                     diff = midPad - ball.y
                     reduc = (leftPad.height / 2) / ball.maxSpeed
                     ball.ySpeed = diff / reduc
 
        elif ball.xSpeed > 0 :
            if ball.y >= rightPad.y and ball.y <= rightPad.y + self.padHeight :
                if ball.x + ball.rad >= rightPad.x :
                    ball.xSpeed *= -1
                    midPad = rightPad.y + self.padHeight / 2
                    diff = midPad - ball.y
                    reduc = (leftPad.height / 2) / ball.maxSpeed
                    ball.ySpeed = diff / reduc

    async def game_state_update(self, event):

        await self.send(text_data=json.dumps({
            'type': 'room',
            'ball_x': event['ball_x'],
            'ball_y': event['ball_y'],
            'left_pad_y': event['left_pad_y'],
            'right_pad_y': event['right_pad_y']
        }))

    async def start_sending_game_state(self):
        while True:
            self.orb.move()
            self.collisions(self.orb, self.leftPad, self.rightPad)
            await self.send_game_state_update()
            await asyncio.sleep(0.1)

    async def stop_sending_game_state(self):
        pass
