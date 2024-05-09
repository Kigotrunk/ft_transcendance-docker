from django.db import models
import threading, time
from random import randint

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

class   pad(models.Model) :

    speed = 5
    def __init__(self, x, y, width, height, bal, diff) :

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.travelTime = 0
        self.algorithm = algorithm(bal, self, diff)
    
    def move(self, up = True):

        if up:
            self.y -= self.speed
        else:
            self.y += self.speed

class   ball(models.Model) :

    maxSpeed = 5

    def __init__(self, x, y, rad):

        self.x = self.ogX = x
        self.y = self.ogY = y
        self.rad = rad
        self.xSpeed = self.maxSpeed
        self.ySpeed = self.maxSpeed
    
    def move(self):

        self.x += self.xSpeed
        self.y += self.ySpeed
    
    def reset(self, leftScore, rightScore, oldScore):

        self.x = self.ogX
        self.y = self.ogY
        self.ySpeed = self.xSpeed
        if leftScore > 1 and leftScore % 2 == 0 and leftScore > oldScore :
            oldScore = leftScore
            self.xSpeed += 1
        if rightScore > 1 and rightScore % 2 == 0 and rightScore > oldScore :
            oldScore = rightScore
            self.xSpeed += 1

    def getxSpeed(self):
        return self.xSpeed

    def resetMenu(self) :

        self.x = self.ogX
        self.y = self.ogY
        self.ySpeed = self.xSpeed
