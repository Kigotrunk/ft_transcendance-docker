from .models import ball, pad, pad_ai, algorithm
import asyncio

class pongGame :

    def __init__(self, room_name, pongConsumer) :
        self.room_name = room_name
        self.room_group_name = f'game_{self.room_name}'
        self.player_number = 1
        self.pongConsumer = pongConsumer
        self.game_state = False
        #self.ids = [pongConsumer.player]
        #self.players = [player_name]
        print("YO!")
        
        
    def __del__(self):
        print("Destructor called")

    async def launchGame(self, mode, diff) :
        print("WESH")
        self.game_task = None
        self.ball = ball(400, 300, 10)
        self.mode = mode 
        self.leftPad = pad(0, 260, 10, 80, self.ball, 2, None)
        self.diff = diff
        if mode == "Online" :
            self.rightPad = pad(790, 260, 10, 80, self.ball, 2, self.leftPad)
            self.player_number = 2
        elif mode == "LM" :
            #self.leftPad = pad_ai(0, 260, 10, 80, self.ball, 2, None)
            self.rightPad = pad_ai(790, 260, 10, 80, self.ball, diff, self.leftPad)
        self.score = [0, 0] 
        self.game_state = True
        self.game_task = asyncio.create_task(self.start_countdown())
        self.game_over = False



    async def start_countdown(self):
        for i in range(3, 0, -1):
            await self.pongConsumer.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'countdown',
                    'countdown': i
                } 
            )
            await asyncio.sleep(1)
        await self.pongConsumer.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'countdown',
                'countdown': "Go!"
            }
        )
        await asyncio.sleep(1)
        await self.pongConsumer.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'countdown',
                'countdown': ""
            }
        )
        await self.game_loop()

    def surv_score_bonus_points(self):
        tmp = self.self.score[0]
        if self.score[0] != tmp :
            self.rightPad.algorithm.surv_score += 42

    async def game_loop(self):
        while True:
            #self.update_ball_position()
            #print("1")
            self.ball.move()
            if self.mode == "Online":
                self.leftPad.move()
                self.rightPad.move()
                print("2")
            elif self.mode == "LM": 
                #print("3")
                self.leftPad.move()
                self.pve()
                if self.diff == 4:
                    print(self.rightPad.algorithm.surv_score)
            #print(self.ball.x)
            #print(self.rightPad.x)
            #print("4")
            self.update_ball_position()
            #print("5")
            self.collisions(self.ball, self.leftPad, self.rightPad)
            #print("6")
            if self.diff == 4 and self.score[1] == 1: 
                self.game_over = True
                print("FINI")
            if self.score[0] == 5 or self.score[1] == 5:
                self.game_over = True
                print("FINI")
            await self.send_game_state()
            await asyncio.sleep(0.01)
            if self.game_over == True:
                time.sleep(0.3)
                del self

    def collisions(self ,ball, leftPad, rightPad):
        if (ball.y + ball.rad >= 600) or (ball.y - ball.rad <= 0) :
            ball.ySpeed *= -1
        if ball.xSpeed < 0 :
            if ball.y >= leftPad.y and ball.y <= leftPad.y + leftPad.height:
                if ball.x - ball.rad <= leftPad.x + leftPad.width :
                    ball.xSpeed *= -1
                    if ball.xSpeed < 8.1 :
                        ball.xSpeed += 0.05
                    midPad = leftPad.y + leftPad.height / 2
                    diff = midPad - ball.y
                    reduc = (leftPad.height / 2) / ball.maxSpeed
                    ball.ySpeed = diff / reduc
        elif ball.xSpeed > 0 :
            if ball.y >= rightPad.y and ball.y <= rightPad.y + rightPad.height:
                if ball.x + ball.rad >= rightPad.x :
                    ball.xSpeed *= -1
                    if ball.xSpeed > -8.1 :
                        ball.xSpeed += -0.05
                    midPad = rightPad.y + rightPad.height / 2
                    diff = midPad - ball.y
                    reduc = (leftPad.height / 2) / ball.maxSpeed
                    ball.ySpeed = diff / reduc

    def     pve(self) :
        if self.ball.xSpeed > 0 :
            #if self.rightPad.algorithm.diff == 4 :
                #self.rightPad.algorithm.hitHeight = self.ball.x
            if self.rightPad.algorithm.replace == 1 :
                self.rightPad.algorithm.hitHeight = 350
            elif self.rightPad.algorithm.replace == 2 :
                self.rightPad.algorithm.hitHeight = 250
            else :
                if self.rightPad.y + self.rightPad.speed + self.rightPad.height <= 600  and self.rightPad.algorithm.hitHeight >= self.rightPad.y + 60:
                    self.rightPad.move(up = False)
                elif self.rightPad.algorithm.hitHeight <= self.rightPad.y + 40  and self.rightPad.y - self.rightPad.speed >= 0:
                    self.rightPad.move(up = True)
            self.rightPad.algorithm.replace = 0
        else :
            if self.rightPad.algorithm.diff > 2 :
                self.rightPad.algorithm.getReadyReplace(self.ball, self.rightPad)
        #if key[pygame.K_z] and leftPad.y - leftPad.speed >= 0 :
            #leftPad.move(up = True)
        #if key[pygame.K_s] and leftPad.y + leftPad.speed + leftPad.height <= winHeight :
            #leftPad.move(up = False)

    def update_ball_position(self):
        if self.ball.x <= 0:
            self.score[1] += 1
            self.reset_all()
        if self.ball.x >= 800:
            self.score[0] += 1
            self.reset_all()
            if self.diff == 4:
                self.rightPad.algorithm.surv_score += 500
                print(self.rightPad.algorithm.surv_score)

    def reset_all(self):
        #self.ball.x, ball.y = [400, 300]
        #self.ball.xSpeed, ball.ySpeed = [0, 0]
        self.ball.reset()
        self.rightPad.y = 260
        self.leftPad.y = 260

    async def send_game_state(self):
        if self.diff == 4 : 
            game_state = {
                'ball_position': [self.ball.x, self.ball.y],
                'paddle1_position': (self.leftPad.y),
                'paddle2_position': (self.rightPad.y),
                'surv_score': (self.rightPad.algorithm.surv_score),
                'game_over': (self.game_state)
            }
        else :
            game_state = {
                'ball_position': [self.ball.x, self.ball.y],
                'paddle1_position': (self.leftPad.y),
                'paddle2_position': (self.rightPad.y),
                'score': self.score,
                'game_over': (self.game_state)
            }
        #print(self.leftPad.y)
        #print(game_state)
        await self.pongConsumer.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_state',
                'game_state': game_state
            }
        )
