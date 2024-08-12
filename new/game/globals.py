#VALUE = CLASSE

queue = []
nb_room = 0
matchmaking_task = None

players = {}
games = {}
cups = {}

def setPlayer(key, value):
    players[key]=value
    
def getPlayer(key):
    if key in players :
        return players[key]
    else :
        return None
    
def removePlayer(key):
    del players[key]

def  setGame(key, value):
    games[key]=value

def getGame(key):
    if key in games :
        return games[key]
    else :
        return None
    
def removeGame(key):
    del games[key]

def setCups(key, value):
    cups[key]=value

def getCup(key):
    if key in cups :
        return cups[key]
    else :
        return None
    
def removeCup(key):
    del cups[key]

# def lunchMatchmaking():
#     global matchmaking_task
#     if matchmaking_task is None or matchmaking_task.done():
#         matchmaking_task = asyncio.create_task(matchmaking(queue))
