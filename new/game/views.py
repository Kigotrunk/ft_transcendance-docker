import sys
from django.shortcuts import render
from asgiref.sync import async_to_sync
from .consumers import GameConsumer
from .models import pad, ball

fps = 60
score  = 10
ballRad = 8
padWidth = 20
padHeight = 100
black = (0, 0, 0)
white = (255, 255, 255)
winWidth = 800
winHeight = 600
"""
def     waitingScreen(ball, rightPad, leftPad, winHeight) :
    if ball.xSpeed < 0 : 
        if  leftPad.y + leftPad.speed + leftPad.height <= winHeight  and leftPad.algorithm.hitHeight >= leftPad.y + 60:
            leftPad.move(up = False)
        elif leftPad.algorithm.hitHeight <= leftPad.y + 40  and leftPad.y - leftPad.speed >= 0:
            leftPad.move(up = True)
    else :
        if rightPad.y + rightPad.speed + rightPad.height <= winHeight  and rightPad.algorithm.hitHeight >= rightPad.y + 60:
            rightPad.move(up = False)
        elif rightPad.algorithm.hitHeight <= rightPad.y + 40  and rightPad.y - rightPad.speed >= 0:
            rightPad.move(up = True)
"""
"""
def     pve(ball, rightPad, leftPad, key, winHeight) :

        if rightPad.y + rightPad.speed + rightPad.height <= winHeight  and rightPad.algorithm.hitHeight >= rightPad.y + 60:
            rightPad.move(up = False)
        elif rightPad.algorithm.hitHeight <= rightPad.y + 40  and rightPad.y - rightPad.speed >= 0:
            rightPad.move(up = True)
        if key[z] and leftPad.y - leftPad.speed >= 0 :
            leftPad.move(up = True)
        if key[s] and leftPad.y + leftPad.speed + leftPad.height <= winHeight :
            leftPad.move(up = False)
"""

def handlePads(key, leftPad, rightPad, show, ball, PVE):
    
    """if show == True : 
        waitingScreen(ball, rightPad, leftPad, winHeight)
    elif show == False and PVE == True : 
        pve(ball, rightPad, leftPad, key, winHeight)"""
    if show == False and PVE == False :
        if key[pygame.K_z] and leftPad.y - leftPad.speed >= 0 :
            leftPad.move(up = True)
        if key[pygame.K_s] and leftPad.y + leftPad.speed + leftPad.height <= winHeight :
            leftPad.move(up = False)

        if key[pygame.K_UP] and rightPad.y - rightPad.speed >= 0 :
            rightPad.move(up = True)
        if key[pygame.K_DOWN] and rightPad.y + rightPad.speed + rightPad.height <= winHeight :
            rightPad.move(up = False)

def collisions(ball, leftPad, rightPad):

    if (ball.y + ball.rad >= winHeight) or (ball.y - ball.rad <= 0) :
        ball.ySpeed *= -1
    
    if ball.xSpeed < 0 :
        if ball.y >= leftPad.y and ball.y <= leftPad.y + padHeight :
            if ball.x - ball.rad <= leftPad.x + padWidth :
                ball.xSpeed *= -1
                midPad = leftPad.y + padHeight / 2
                diff = midPad - ball.y
                reduc = (leftPad.height / 2) / ball.maxSpeed
                ball.ySpeed = diff / reduc
    
    elif ball.xSpeed > 0 :
        if ball.y >= rightPad.y and ball.y <= rightPad.y + padHeight :
            if ball.x + ball.rad >= rightPad.x :
                ball.xSpeed *= -1
                midPad = rightPad.y + padHeight / 2
                diff = midPad - ball.y
                reduc = (leftPad.height / 2) / ball.maxSpeed
                ball.ySpeed = diff / reduc

def game(pve = True, diff = 2) :

    rightScore, leftScore, oldScore, timer, end = 0, 0, 0, 0, 0
    bal = ball(winWidth // 2, winHeight // 2, 10)
    leftPad = pad(10, winHeight // 2 - padHeight // 2, padWidth, padHeight, bal, diff)
    rightPad = pad(winWidth - 10 - padWidth, winHeight // 2 - padHeight // 2, padWidth, padHeight, bal, diff)
    
    while True :

        bal.move()
        #key = pygame.key.get_pressed()
        collisions(bal, leftPad, rightPad)
        #handlePads(key, leftPad, rightPad, False, bal, pve)
        
        if bal.x < 0 :

            if diff == 4 :
                end = -1
            elif rightScore < 10 :
                rightScore += 1
                bal.reset(leftScore, rightScore, oldScore)
        
        elif bal.x > winWidth :

            if diff == 4 :
                bal.resetMenu()
            elif leftScore < 10 :
                leftScore += 1
                bal.reset(leftScore, rightScore, oldScore)
        
        async_to_sync(game_consumer.update_game)({
            
            'message': {
                
                'ball_x': bal.x,
                'ball_y': bal.y,
                'left_pad_y': leftPad.y,
                'right_pad_y': rightPad.y
            }
        })
        #screen(win, [leftPad, rightPad], bal, False, None, diff, end, timer, leftScore, rightScore)

def pong(request):
    
    return render(request, "game/game.html")