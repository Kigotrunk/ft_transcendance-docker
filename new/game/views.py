
fps = 60
score  = 10
ballRad = 8 # à redefinir
padWidth = 20 # à redefinir
padHeight = 100 # à redefinir
black = (0, 0, 0)
white = (255, 255, 255)
winWidth = 800 # à redefinir
winHeight = 600 # à redefinir

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

from django.shortcuts import render

def rooms(request):
    return render(request, 'rooms.html')

def game(request, room_name):
    return render(request, 'game.html', {'room_name': room_name})
