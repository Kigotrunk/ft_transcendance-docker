from .models import ball, pad, pad_ai, algorithm, partie 
import asyncio
import time
import json
from channels.db import database_sync_to_async
from myaccount.models import Account
from .globals import setGame, getGame, removeGame, setCups, getCup, removeCup, setPlayer, getPlayer, removePlayer, queue, nb_room, players, games, cups, matchmaking_task
import threading, time
from chat.consumers import chat_consumers

class pongGame :

    def __init__(self, room_name, pongConsumer) :
        self.room_name = room_name
        self.room_group_name = f'game_{self.room_name}'
        self.player_number = 1
        self.pongConsumer = pongConsumer
        self.game_state = False
        self.left_player = None
        self.right_player = None
        self.dc_side = None
        self.test = False
        self.tournament = None
        #self.ids = [pongConsumer.player]
        #self.players = [player_name]
        
        
    def __del__(self):
        print("Destructor called")

    async def launchGame(self, mode, diff, is_cup, pongConsumer) :
        print("Launching game")
        self.game_task = None
        self.ball = ball(400, 300, 10)
        self.mode = mode
        self.leftPad = pad(0, 260, 10, 80, self.ball, 2, None)
        self.diff = diff
        self.rightConsumer = pongConsumer
        if mode == "Online" :
            self.rightPad = pad(790, 260, 10, 80, self.ball, 2, self.leftPad)
            self.player_number = 2
            await self.save_is_in_game(self.left_player)
            await self.save_is_in_game(self.right_player)
            self.left_player.in_lobby = True
            self.right_player.in_lobby = True
        elif mode == "LM" :
            await self.save_is_in_game(self.left_player)
            #self.leftPad = pad_ai(0, 260, 10, 80, self.ball, 2, None)
            self.left_player.in_lobby = True
            self.rightPad = pad_ai(790, 260, 10, 80, self.ball, diff, self.leftPad)
        self.score = [0, 0]
        self.game_over = False
        self.game_state = True
        self.is_cup = is_cup
        self.echanges_moyen = 0
        self.order_points_scored = []
        self.time_per_point = 0
        self.lock = threading.Lock()
        self.thd_for_time = threading.Thread(target=self.monitoring_time_per_point, args=(), daemon=True)
        self.thd_for_time.start()
        self.timers = []
        self.is_ff = False
        self.goal = False
        self.nombres_echange = []  
        if is_cup == True:
            asyncio.create_task(self.waiting_cup_opponents())
        else:
            self.game_task = asyncio.create_task(self.start_countdown())

    def monitoring_time_per_point(self):
        if (self.is_cup == True):
            time.sleep(64)
        else :
            time.sleep(4)
        while True : 
            self.time_per_point += 1
            if self.goal == True :
                self.timers.append(self.time_per_point)
                self.time_per_point = 0
                self.goal = False
            if self.is_ff == True or self.game_over == True :
                return
            time.sleep(1)
	

    async def waiting_cup_opponents(self):
        i = 10
        while(i > 0):
            await asyncio.sleep(1)
            i-= 1
            await self.pongConsumer.channel_layer.group_send(
                self.room_group_name,
                {
                'type': 'next_game_countdown',
                'next_game_countdown': {
                    'type': 'next_game_countdown',
                    'message': f"{i}"
                }
            } 
            )
            if i < 10 :
                if self.left_player.id in chat_consumers:
                    await chat_consumers[self.left_player.id].send(text_data=json.dumps(
                        {
                            'message' : f"{i}",
                            'issuer': "Tournament Info",
                            'receiver' : self.left_player.name
                        }
                    ))
                if self.right_player.id in chat_consumers:
                    await chat_consumers[self.right_player.id].send(text_data=json.dumps(
                        {
                            'message' : f"{i}",
                            'issuer': "Tournament Info",
                            'receiver' : self.right_player.name
                        }
                    ))

        asyncio.create_task(self.start_countdown())

    async def start_countdown(self):
        print("Starting countdown")
        if self.mode != 'LM':
            print("Sending game info")
            await self.left_player.consumers.send(text_data=json.dumps({'test': 'test'}))
            await self.pongConsumer.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_info',
                    'game_info': {
                        'type': 'game_info',
                        'left': self.left_player.id,
                        'right': self.right_player.id,
                        'left_username': self.left_player.name,
                        'right_username': self.right_player.name,
                    }
                }
            )
        print("Sending countdown")
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
            if self.ball :
                self.ball.move()
            if self.mode == "Online":
                self.leftPad.move()
                self.rightPad.move()
            elif self.mode == "LM": 
                self.leftPad.move()
                self.pve()
            self.update_ball_position()
            self.collisions(self.ball, self.leftPad, self.rightPad)
            if self.diff == 4 and self.score[1] == 1: 
                self.game_over = True
            if self.score[0] == 5 or self.score[1] == 5 or self.test == True :
                if self.test == True :
                    if self.dc_side == 'left' :
                        self.score[1] = 5
                    elif self.dc_side == 'right' :
                        self.score[0] = 5 
                self.game_over = True
            await self.send_game_state()
            if self.game_over == True:
                if self.mode != "LM":
                    await self.save_game_result()
                winner = self.left_player if self.score[0] == 5 else self.right_player
                loser = self.left_player if self.score[0] != 5 else self.right_player
                if self.mode != "LM":
                    self.timers.append(self.time_per_point + 1)
                    await self.send_game_result(winner, loser)
                    if self.is_cup == True :
                        await self.save_is_not_in_game(loser)
                    else :
                        await self.save_is_not_in_game(winner)
                        await self.save_is_not_in_game(loser)
                    self.left_player.in_lobby = False
                    self.right_player.in_lobby = False
                    if self.tournament:
                        await self.tournament.match_result(self.room_name, winner, loser)
                else :
                    await self.send_game_result(winner, loser)
                    if self.diff == 4 :
                        await self.save_survivor_score()
                    await self.save_is_not_in_game(self.left_player)
                    self.rightPad.algorithm.dedge = True
                    self.left_player.in_lobby = False
                    del self.rightPad.algorithm
                del self.leftPad
                del self.rightPad
                del self.ball
                print("end of game")
                removeGame(self.room_name)
                del self
                break
            await asyncio.sleep(0.01)

    def collisions(self ,ball, leftPad, rightPad):
        if (ball.y + ball.rad >= 600) or (ball.y - ball.rad <= 0) :
            ball.ySpeed *= -1
        if ball.xSpeed < 0 :
            if ball.y >= leftPad.y and ball.y <= leftPad.y + leftPad.height:
                if ball.x - ball.rad <= leftPad.x + leftPad.width :
                    ball.xSpeed *= -1
                    if ball.xSpeed < 8.1 :
                        ball.xSpeed += 0.2
                    midPad = leftPad.y + leftPad.height / 2
                    diff = midPad - ball.y
                    reduc = (leftPad.height / 2) / ball.maxSpeed
                    ball.ySpeed = diff / reduc
                    self.echanges_moyen += 1
        elif ball.xSpeed > 0 :
            if ball.y >= rightPad.y and ball.y <= rightPad.y + rightPad.height:
                if ball.x + ball.rad >= rightPad.x :
                    ball.xSpeed *= -1
                    if ball.xSpeed > -8.1 :
                        ball.xSpeed += -0.2
                    midPad = rightPad.y + rightPad.height / 2
                    diff = midPad - ball.y
                    reduc = (leftPad.height / 2) / ball.maxSpeed
                    ball.ySpeed = diff / reduc
                    self.echanges_moyen += 1

    def pve(self) :
        if self.ball.xSpeed > 0 :
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

    def update_ball_position(self):
        if self.ball.x <= 0:
            self.score[1] += 1
            self.reset_all()
            if self.mode != "LM" : 
                self.order_points_scored.append(self.right_player.id)
            if self.mode == "LM" :
                self.rightPad.algorithm.hitHeight = 300
        if self.ball.x >= 800:
            self.score[0] += 1
            self.reset_all()
            if self.mode != "LM" : 
                self.order_points_scored.append(self.left_player.id)
            if self.mode == "LM" : 
                self.rightPad.algorithm.hitHeight = 300
            if self.diff == 4:
                self.rightPad.algorithm.surv_score += 500

    def reset_all(self):
        self.ball.reset()
        self.rightPad.y = 260
        self.leftPad.y = 260
        self.goal = True
        self.nombres_echange.append(self.echanges_moyen)
        self.echanges_moyen = 0

    async def save_survivor_score(self) :
        player = await database_sync_to_async(Account.objects.get)(id=self.left_player.id)
        if player.highest_score < self.rightPad.algorithm.surv_score :
            player.highest_score = self.rightPad.algorithm.surv_score
            await database_sync_to_async(player.save)()
        return 

    async def send_game_state(self):
        if self.diff == 4 : 
            game_state = {
                'type' : 'game_state',
                'ball_position': [self.ball.x, self.ball.y],
                'paddle1_position': (self.leftPad.y),
                'paddle2_position': (self.rightPad.y),
                'surv_score': (self.rightPad.algorithm.surv_score),
                'game_over': (self.game_over)
            }
        else :
            game_state = {
                'type' : 'game_state',
                'ball_position': [self.ball.x, self.ball.y],
                'paddle1_position': (self.leftPad.y),
                'paddle2_position': (self.rightPad.y),
                'score': self.score,
                'game_over': (self.game_over)
            }
        await self.pongConsumer.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_state',
                'game_state': game_state
            }
        )
    
    async def send_game_result(self, winner, loser):
        if self.is_cup == True:
            game_result = {
                'mode' : "cup",
                'winner' : winner.id,
                'winner_elo' : winner.elo,
                'loser' : loser.id,
                'loser_elo' : loser.elo,
                'score' : self.score
            }
        else:
            if self.mode == "Online":
                game_result = {
                    'mode' : "duel",
                    'winner' : winner.id,
                    'winner_elo' : winner.elo,
                    'loser' : loser.id,
                    'loser_elo' : loser.elo,
                    'score' : self.score
                }
            else:
                    game_result = {
                        'mode' : "ia",
                        'win' : False if winner == None else True,
                        'diff' : self.diff,
                        'score' : f"{self.score[0]} - {self.score[1]}" if self.diff != 4 else self.rightPad.algorithm.surv_score,
                    }

        await self.pongConsumer.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_result',
                'game_result' : game_result
            }
        )
    
    def set_tournament(self, tournament):
        self.tournament = tournament

    async def save_is_in_game(self, player):
        user = await database_sync_to_async(Account.objects.get)(id=player.id)
        user.is_in_game = True
        await database_sync_to_async(user.save)()

    async def save_is_not_in_game(self, player):
        user = await database_sync_to_async(Account.objects.get)(id=player.id)
        user.is_in_game = False
        await database_sync_to_async(user.save)()

    async def save_game_result(self):
        user1 = await database_sync_to_async(Account.objects.get)(id=self.left_player.id)
        user2 = await database_sync_to_async(Account.objects.get)(id=self.right_player.id)
        total = sum(self.nombres_echange)
        moyenne = total / 5
        await database_sync_to_async(partie.objects.create)(
            player1 = user1,
            player2 = user2,
            score_player1=self.score[0],
            score_player2=self.score[1],
            moyenne_echange=moyenne,
            order_points_scored=self.order_points_scored,
            timers=self.timers, 
            nb_echange_per_point=self.nombres_echange
        )

        left_win = 1
        right_win = 0
        if self.score[0] < self.score[1]:
            left_win = 0
            right_win = 1

        print("Calculating new elo ...")

        new_left_elo = round(user1.elo + user1.coef * (left_win - (1 / (1 + 10 ** ((user2.elo - user1.elo) / 400)))))
        print(f"Old elo : {user1.elo}\nNew elo : {new_left_elo}")
        new_right_elo = round(user2.elo + user2.coef * (right_win - (1 / (1 + 10 ** ((user2.elo - user1.elo) / 400)))))
        print(f"Old elo : {user2.elo}\nNew elo : {new_right_elo}")

        if self.score[0] > self.score[1]:
            print(f"Updating left player's stats...")
            self.left_player.elo = new_left_elo
            await self.update_player_stats(user1.id, win=True, new_elo=new_left_elo)
            print(f"Updating right player's stats...")
            self.right_player.elo = new_right_elo
            await self.update_player_stats(user2.id, win=False, new_elo=new_right_elo)
        else:
            print(f"Updating left player's stats...")
            self.left_player.elo = new_left_elo
            await self.update_player_stats(user1.id, win=False, new_elo=new_left_elo)
            print(f"Updating right player's stats...")
            self.right_player.elo = new_right_elo
            await self.update_player_stats(user2.id, win=True, new_elo=new_right_elo)
        

    async def update_player_stats(self, player_id, win, new_elo):
        
        player = await database_sync_to_async(Account.objects.get)(id=player_id)
        
        if win:
            player.nb_win += 1
        else:
            player.nb_loose += 1

        player.nb_games += 1
        player.elo = new_elo

        if player.nb_games > 30:
            player.coef = 20
        elif player.elo > 2400:
            player.coef = 10

        await database_sync_to_async(player.save)()

        print(f"Player {player.username} : ")
        print(f"Number of win(s) : {player.nb_win}")
        print(f"Number of Loss(es) : {player.nb_loose}")
        print(f"Number of games played : {player.nb_games}")
        print(f"Player's new elo : {player.elo}")
        print(f"Player's new coef : {player.coef}")

async def matchmaking(queue):

    elo_range = 40
    print('Entering matchmaking...')

    async def get_updated_elo(player):
        user = await database_sync_to_async(Account.objects.get)(id=player.id)
        player.elo = user.elo
        return player

    while len(queue) > 0:

        print(f'List of players in queue : {queue}')

        if len(queue) == 1:
            print('Only one player in queue')
        
        elif len(queue) > 1:

            print('Sorting players by time spent on queue ...')
            sorted_queue = sorted(queue, key=lambda player: player.wait_time, reverse=True)
            updated_queue = await asyncio.gather(*[get_updated_elo(player) for player in sorted_queue])
            for player in sorted_queue:
                print(f'{player.name} with {round(time.time() - player.wait_time)} second(s)')
            
            for i, player1 in enumerate(updated_queue):

                match_found = False
                while not match_found and len(queue) > 1:

                    start_time = time.time()
                    while time.time() - start_time < 3:

                        print('Searching potentials players within 3 seconds ...')
                        sorted_queue = sorted(queue, key=lambda player: player.wait_time, reverse=True)
                        for player2 in sorted_queue[i+1:]:

                            print('Comparing elo ...')
                            print(f'player 1 elo : {player1.elo}')
                            print(f'player 2 elo : {player2.elo}')
                            if (player1 and player2) and (player1 != player2 and abs(player1.elo - player2.elo) <= elo_range):

                                queue.remove(player1)
                                queue.remove(player2)
                                sorted_queue.remove(player1)
                                sorted_queue.remove(player2)
                                match_found = True
                                print('Match found ! Removing 2 players from queue ...')
                                match_info = {
                                    'action': 'match_found',
                                    'players': [player1.id, player2.id]
                                }
                                await player1.consumers.send(text_data=json.dumps(match_info))
                                await player2.consumers.send(text_data=json.dumps(match_info))
                                print('Launching match in distincted task ...')
                                await player1.join_match()
                                await player2.join_match()
                                global nb_room
                                nb_room += 1
                                break
                        
                        if match_found or len(queue) < 2:
                            break

                        await asyncio.sleep(0.1)
                    
                    if match_found is False and len(queue) > 1:
                        
                        print('No player found within elo range ! Increasing elo range ...')
                        elo_range += 40
                    
                    else:
                        break
                    
                if match_found or len(queue) > 1:
                    break

        await asyncio.sleep(1)