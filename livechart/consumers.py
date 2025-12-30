# livechart/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LiveChartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "live_chart"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_chart_data(self, event):
        await self.send(text_data=json.dumps(event["data"]))
