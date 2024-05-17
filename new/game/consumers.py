import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ball, pad

class player(AsyncWebsocketConsumer):

    padWidth = 20  # à redefinir
    padHeight = 100  # à redefinir
    winWidth = 800  # à redefinir
    winHeight = 600  # à redefinir

    players = {}
    orb = ball(winWidth // 2, winHeight // 2, 0)
    leftPad = pad(0, winHeight // 2 - padHeight // 2, padWidth, padHeight, 0, 0)
    rightPad = pad(winWidth - padWidth, winHeight // 2 - padHeight // 2, padWidth, padHeight, 0, 0)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name
        if self.room_name not in self.players:
            self.players[self.room_name] = 1
            self.side = 'left'
        else:
            self.players[self.room_name] += 1
            self.side = 'right'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        self.sending = True
        await self.start_sending_game_state()

    async def disconnect(self):
        self.sending = False
        self.players[self.room_name] -= 1
        if self.players[self.room_name] == 0:
            del self.players[self.room_name]
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']
        
        if self.side == 'left':
            if message_type == 'z' and self.leftPad.y - self.leftPad.speed >= 0:
                self.leftPad.move(up=True)
            if message_type == 's' and self.leftPad.y + self.leftPad.speed + self.leftPad.height <= self.winHeight:
                self.leftPad.move(up=False)
        elif self.side == 'right':
            if message_type == 'z' and self.rightPad.y - self.rightPad.speed >= 0:
                self.rightPad.move(up=True)
            if message_type == 's' and self.rightPad.y + self.rightPad.speed + self.rightPad.height <= self.winHeight:
                self.rightPad.move(up=False)
        else:
            return

        if message_type == 'z' and self.leftPad.y - self.leftPad.speed >= 0:
            self.leftPad.move(up=True)
        if message_type == 's' and self.leftPad.y + self.leftPad.speed + self.leftPad.height <= self.winHeight:
            self.leftPad.move(up=False)
        if message_type == 'UP' and self.rightPad.y - self.rightPad.speed >= 0:
            self.rightPad.move(up=True)
        if message_type == 'DOWN' and self.rightPad.y + self.rightPad.speed + self.rightPad.height <= self.winHeight:
            self.rightPad.move(up=False)

    async def send_game_state_update(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_state_update',
                'ball_x': self.orb.x,
                'ball_y': self.orb.y,
                'left_pad_y': self.leftPad.y,
                'right_pad_y': self.rightPad.y
            }
        )

    def collisions(self, ball, leftPad, rightPad):
        if (ball.y + ball.rad >= self.winHeight) or (ball.y - ball.rad <= 0):
            ball.ySpeed *= -1

        if ball.xSpeed < 0:
            if leftPad.y <= ball.y <= leftPad.y + leftPad.height:
                if ball.x - ball.rad <= leftPad.x + leftPad.width:
                    ball.xSpeed *= -1
                    midPad = leftPad.y + leftPad.height / 2
                    diff = midPad - ball.y
                    reduc = (leftPad.height / 2) / ball.maxSpeed
                    ball.ySpeed = diff / reduc
            elif ball.x - ball.rad <= 0:
                ball.reset()

        elif ball.xSpeed > 0:
            if rightPad.y <= ball.y <= rightPad.y + rightPad.height:
                if ball.x + ball.rad >= rightPad.x:
                    ball.xSpeed *= -1
                    midPad = rightPad.y + rightPad.height / 2
                    diff = midPad - ball.y
                    reduc = (rightPad.height / 2) / ball.maxSpeed
                    ball.ySpeed = diff / reduc
            elif ball.x + ball.rad >= self.winWidth:
                ball.reset()

    async def game_state_update(self, event):
        await self.send(text_data=json.dumps({
            'ball_x': event['ball_x'],
            'ball_y': event['ball_y'],
            'left_pad_y': event['left_pad_y'],
            'right_pad_y': event['right_pad_y']
        }))

    async def start_sending_game_state(self):
        while self.sending:
            self.orb.move()
            self.collisions(self.orb, self.leftPad, self.rightPad)
            print(f"Sending game state: Ball at ({self.orb.x}, {self.orb.y}), Left pad at {self.leftPad.y}, Right pad at {self.rightPad.y}")
            await self.send_game_state_update()
            await asyncio.sleep(1/60)

    async def stop_sending_game_state(self):
        self.sending = False
