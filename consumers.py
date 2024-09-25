import json
from django.core import serializers
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from counter import views


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
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        a,i = message.split(',')
        if 'addlog' == a:
            views.add_log(None, int(i))
        if 'take_a_break' == a:
            views.take_a_break(None, int(i))
        if 'lane' in a:
            d,lane = a.split(':')
            views.back_to_swim(None, int(i), int(lane))
        # Send message to count group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "count.message", "message": 'dummy'}
        )


    # Receive message from count group
    def count_message(self, event):
        # print('Receive message from count group')
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))



