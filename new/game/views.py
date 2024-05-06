from django.shortcuts import render
import pygame, sys
from .models import pad, ball, Button

pygame.init()

fps = 60
score  = 10
ballRad = 8
padWidth = 20
padHeight = 100
black = (0, 0, 0)
white = (255, 255, 255)
winWidth = 800
winHeight = 600
scoreFont = pygame.font.SysFont("comicsans", 50)

playButton = Button(winWidth // 2, (winHeight // 2) - 60, "PLAY", pygame.font.SysFont("comicsans", 25), white)

soloButton = Button(winWidth // 2, (winHeight // 2) - 90, "SOLO", pygame.font.SysFont("comicsans", 25), white)
versusButton = Button(winWidth // 2, (winHeight // 2) - 30, "VERSUS", pygame.font.SysFont("comicsans", 25), white)
onlineButton = Button(winWidth // 2, (winHeight // 2) + 30, "ONLINE", pygame.font.SysFont("comicsans", 25), white)
backPlayButton = Button(winWidth // 2, (winHeight // 2) + 90, "BACK", pygame.font.SysFont("comicsans", 25), white)

easyButton = Button(winWidth // 2, (winHeight // 2) - 120, "EASY", pygame.font.SysFont("comicsans", 25), white)
mediumButton = Button(winWidth // 2, (winHeight // 2) - 60, "MEDIUM", pygame.font.SysFont("comicsans", 25), white)
hardButton = Button(winWidth // 2, winHeight // 2, "HARD", pygame.font.SysFont("comicsans", 25), white)
survivalButton = Button(winWidth // 2, (winHeight // 2) + 60, "SURVIVE !", pygame.font.SysFont("comicsans", 25), white)
backOptionButton = Button(winWidth // 2, (winHeight // 2) + 120, "BACK", pygame.font.SysFont("comicsans", 25), white)

quitButton = Button(winWidth // 2, (winHeight // 2) + 60, "EXIT", pygame.font.SysFont("comicsans", 25), white)
afterGame = Button(winWidth // 2, (winHeight // 2) + 60, "BACK TO MENU", pygame.font.SysFont("comicsans", 25), white)

win = pygame.display.set_mode((winWidth, winHeight))

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

def     pve(ball, rightPad, leftPad, key, winHeight) :
        print(rightPad.algorithm.hitHeight)
        if rightPad.y + rightPad.speed + rightPad.height <= winHeight  and rightPad.algorithm.hitHeight >= rightPad.y + 60:
            rightPad.move(up = False)
        elif rightPad.algorithm.hitHeight <= rightPad.y + 40  and rightPad.y - rightPad.speed >= 0:
            rightPad.move(up = True)
        if key[pygame.K_z] and leftPad.y - leftPad.speed >= 0 :
            leftPad.move(up = True)
        if key[pygame.K_s] and leftPad.y + leftPad.speed + leftPad.height <= winHeight :
            leftPad.move(up = False)

def handlePads(key, leftPad, rightPad, show, ball, PVE):
    
    if show == True : 
        waitingScreen(ball, rightPad, leftPad, winHeight)
    elif show == False and PVE == True : 
        pve(ball, rightPad, leftPad, key, winHeight)
    elif show == False and PVE == False :
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

def screen(win, padTab, ball, inMenu, buttons, diff, end, timer, leftScore, rightScore) :

    win.fill(black)

    for pad in padTab :
        pad.sprite(win, white)
    
    ball.sprite(win, white)

    if inMenu is False and diff != 4:

        pygame.draw.rect(win, white, (winWidth // 2 - 3, 0, 6, winHeight // 2 - 20))
        pygame.draw.rect(win, white, (winWidth // 2 - 3, winHeight // 2 + 20, 6, winHeight // 2 - 20))
        pygame.draw.circle(win, white, (winWidth // 2, winHeight // 2), 24)
        pygame.draw.circle(win, black, (winWidth // 2, winHeight // 2), 18)
        pygame.draw.circle(win, white, (winWidth // 2, winHeight // 2), 3)
    
    elif inMenu is True :

        for button in buttons:
            button.update(win)
        
    if diff == 4 and inMenu is False:

        win.blit(timer, (winWidth // 2 - timer.get_width() // 2, 20))

        if end == 1 :

            textWon = pygame.font.SysFont(None, 60).render(str("YOU WIN !"), True, white)
            win.blit(textWon, (winWidth // 2 - textWon.get_width() // 2, winHeight // 2 - textWon.get_height() - 60))
            afterGame.update(win)
        
        elif end == -1 :

            textLost = pygame.font.SysFont(None, 60).render(str("YOU LOST !"), True, white)
            win.blit(textLost, (winWidth // 2 - textLost.get_width() // 2, winHeight // 2 - textLost.get_height() - 60))
            afterGame.update(win)
    
    elif diff != 4 and inMenu is False:

        leftText = scoreFont.render(f"{leftScore}", 1, white)
        rightText = scoreFont.render(f"{rightScore}", 1, white)
        win.blit(leftText, (winWidth // 4 - leftText.get_width() // 2, 20))
        win.blit(rightText, (winWidth * (3 / 4 ) - rightText.get_width() // 2, 20))

    pygame.display.update()

def run(pve = True, diff = 2) :

    start = pygame.time.get_ticks()
    refreshRate = pygame.time.Clock()
    rightScore, leftScore, oldScore, timer, end = 0, 0, 0, 0, 0
    bal = ball(winWidth // 2, winHeight // 2, 10)
    leftPad = pad(10, winHeight // 2 - padHeight // 2, padWidth, padHeight, bal, diff)
    rightPad = pad(winWidth - 10 - padWidth, winHeight // 2 - padHeight // 2, padWidth, padHeight, bal, diff)
    
    while True :

        refreshRate.tick(fps)
        bal.move()
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        collisions(bal, leftPad, rightPad)
        handlePads(key, leftPad, rightPad, False, bal, pve)

        if diff == 4 :

            remaining = max(fps - (pygame.time.get_ticks() - start) // 1000, 0)
            timer = pygame.font.SysFont(None, 50).render(str(remaining), True, white)
            if remaining <= 0 :
                end = 1
        
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
        
        elif leftScore == 10 or rightScore == 10 and diff != 4:
            launch()

        for event in pygame.event.get():

            if event.type is pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if afterGame.checkForInput(mouse) and end == 1 or end == -1 :
                    launch()
        
        screen(win, [leftPad, rightPad], bal, False, None, diff, end, timer, leftScore, rightScore)

def launch() :

    refreshRate = pygame.time.Clock()

    bal = ball(winWidth // 2, winHeight // 2, 10)
    leftPad = pad(10, winHeight // 2 - padHeight // 2, padWidth, padHeight, bal, 2)
    rightPad = pad(winWidth - 10 - padWidth, winHeight // 2 - padHeight // 2, padWidth, padHeight, bal, 2)
    toPrint = (playButton, quitButton)

    while True :

        refreshRate.tick(fps)
        mouse = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()
        handlePads(key, leftPad, rightPad, True, bal, False)
        bal.move()
        collisions(bal, leftPad, rightPad)
        if bal.x < 0 :
            bal.resetMenu()
        elif bal.x > winWidth :
            bal.resetMenu()

        for event in pygame.event.get():
            
            if event.type is pygame.QUIT:
                
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if playButton.checkForInput(mouse):
                    toPrint = (soloButton, versusButton, onlineButton, backPlayButton)
                
                elif backPlayButton.checkForInput(mouse):
                    toPrint = (playButton, quitButton)
                
                elif soloButton.checkForInput(mouse):
                    toPrint = (easyButton, mediumButton, hardButton, survivalButton, backOptionButton)
                
                elif backOptionButton.checkForInput(mouse):
                    toPrint = (soloButton, versusButton, onlineButton, backPlayButton)

                elif easyButton.checkForInput(mouse):
                    run(diff=1)

                elif mediumButton.checkForInput(mouse):
                    run(diff=2)

                elif hardButton.checkForInput(mouse):
                    run(diff=3)
                
                elif survivalButton.checkForInput(mouse):
                    run(diff=4)

                elif versusButton.checkForInput(mouse):
                    run(pve=False)

                elif quitButton.checkForInput(mouse):
                    pygame.quit()
                    sys.exit()

        screen(win, (leftPad, rightPad), bal, True, toPrint, None, None, None, None, None)

def game(request) :
    launch()
    return render(request, 'home.html')