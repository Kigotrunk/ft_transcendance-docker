
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

from asgiref.sync import async_to_sync
from django.shortcuts import render
from channels.layers import get_channel_layer

def lobby(request):
    return render(request, "game/game.html")

def room(request, room_name):
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "game_%s" % room_name,
        {
            "type": "game_state_update",
            "ball_x": winWidth // 2,
            "ball_y": winHeight // 2,
            "left_pad_y": winHeight // 2 - padHeight // 2,
            "right_pad_y": winHeight // 2 - padHeight // 2,
        }
    )
    return render(request, "game/room.html", {"room_name": room_name})
