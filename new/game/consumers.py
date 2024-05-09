import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class GameConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass

    def update_game(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))

# le client rejoins d'abord un channel et quitte le channel avant de disconnect()