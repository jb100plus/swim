import json
from django.core import serializers
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime


class CountConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name  = "counter"
        self.room_group_name = "countergroup"
        # join group
        print(f'connected {self.room_group_name}')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print('Receive message from WebSocket')
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "count.message", "message": 'dummy'}
        )


    # Receive message from room group
    def count_message(self, event):
        # print('Receive message from room group')
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))



