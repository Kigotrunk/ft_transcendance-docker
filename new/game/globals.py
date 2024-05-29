#VALUE = CLASSE

games = {}
def  setGame(key, value):
    games[key]=value


def getGame(key):
    if key in games :
        return games[key]
    else :
        return None
    
def removeGame(key):
    del games[key]


