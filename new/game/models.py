from django.db import models
import threading, time
from random import randint
"""
class algorithm(models.Model) : 
    
    #data order, Switch, difficulty, actualRng, smartShots, adaptation#
    #showMatchMenu = True
    #playerVsIA = False
    #playerVsPlayer = False
    #lock = threading.Lock()
    #ePointList = []
    #diff = 2
    #thd = threading.Thread()
    #thd.start()

    def __init__(self, ball, pad, diff) :
        switch = True
        self.diff = diff
        self.thd = threading.Thread(target=self.monitoringIaView, args=(ball, pad), daemon=True)
        self.thd.start()
        self.hitHeight = self.getLandingPlace(ball, pad)

    def getThread(self):
        return self.thd
        
    def getDiff(self) :
        return self.diff

    def getLandingPlace(self, ball, Pad):
        if self.diff == 1 or self.diff == 2:
            travelTime = (Pad.x - ball.x) / ball.xSpeed
            hitHeight = ball.y + ball.ySpeed * travelTime
        else :
            travelTime = (Pad.x - ball.x) / ball.xSpeed
            hitHeight = ball.y + ball.ySpeed * travelTime
            #changer pour Calculer les rebons a l'avance#
        return hitHeight
        #print(self.hitHeight)
        #self.ePointList.append(self.endpoint)
        #print("AAA")
    
    def smartShot(self, ball, playerPad):
        if playerPad.y < 205 :
            return (0)
        elif playerPad.y > 395 :
            return (1)
        else :
            return (2)
            
    def suvivalImprovement(self, algorithm, ball) :
        if ball.x > 800 :
            algorithm.data[3] += 1
        
    def assistanceLowerDificulty(self, leftScore, rightScore) :
        tmp = leftScore
        tmp2 = rightScore
        while leftScore == tmp :
            if rightScore > leftScore + 3 :
                #ASK IF PLAYER WANTS The game to be easier ???
                self.data[3] -= 3
                self.data[2] -= 2
                if self.data[2] < 9 :
                    self.data[5] = False
    def result():
        print("A")
    
    def monitoringIaView(self, ball, Pad) :
        while True :
            self.hitHeight = self.getLandingPlace(ball, Pad)
            #self.whereToGoAi(ball, Pad)
            #print(self.hitHeight)
            time.sleep(1)
            #while self.showMatchMenu == True :
        #thd.join()


        
    def whereToGoAi(self, ball, Pad):
        #rng = 4
        travelTime = (Pad.x - ball.x) / ball.xSpeed
        Pad.algorithm.hitHeight = ball.y + ball.ySpeed * Pad.travelTime
        #self.getLandingPlace(ball, Pad)
        #print(Pad.algorithm.data[2])
        #if Pad.algorithm.endpoint == 300 :
            #rng = 7
        #if Pad.difficulty == "hard":
            #rng = 15
        #self.thd.start()
        #print(Pad.oPif)
        #tout ce qu'il y a en dessous risque de changer de place apres l'ajout d'autres algorithms
        #if Pad.oPif == rng - 1:
            #if Pad.hitHeight > 300:
             #   if Pad.difficulty == "hard" :
                 #   Pad.hitHeight-= 78
                #elif Pad.difficulty == "medium" :
                #    Pad.hitHeight-= 86
                #else :
               #     Pad.hitHeight -= 100
         #   else:
         #       if Pad.difficulty == "hard" :
       #             Pad.hitHeight += 78
     #           elif Pad.difficulty == "medium" :
           #         Pad.hitHeight += 86
        #        else :
          #          Pad.hitHeight += 100

    def canLoseRng(self) :
        rng = randint(0, self.data[3])
        if rng == self.data[3] - 1 :
            return True
"""

class   pad:

    speed = 1
    def __init__(self, x, y, width, height, bal, diff, playerPad) :

        self.x = self.ogX = x
        self.y = self.ogY = y
        self.width = width
        self.height = height
        self.travelTime = 0
        #self.algorithm = algorithm(bal, self, diff, playerPad)


    def sprite(self, win, color):

        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))

    def move(self, up = True):

        if up:
            if self.y > 0 :
                self.y -= 10
        else:
            if self.y < 520 :
                self.y += 10

    def reset(self):

        self.x = self.ogX
        self.y = self.ogY

class   ball:

    maxSpeed = 6

    def __init__(self, x, y, rad):

        self.x = self.ogX = x
        self.y = self.ogY = y
        self.rad = rad
        self.xSpeed = self.maxSpeed
        self.ySpeed = 0

    def sprite(self, win, color):

        pygame.draw.circle(win, color, (self.x, self.y), self.rad)

    def move(self):

        self.x += self.xSpeed
        self.y += self.ySpeed

    def reset(self):

        self.x = self.ogX
        self.y = self.ogY
        #self.xSpeed = self.maxSpeed
        if self.xSpeed > 5 :
            self.xSpeed = 6
        elif self.xSpeed < -5 :
            self.xSpeed = -6
        self.ySpeed = 0

    def getxSpeed(self):
        return self.xSpeed