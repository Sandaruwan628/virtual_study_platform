import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WhiteboardConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.board_id = None

    async def connect(self):
        # Get board ID from the URL
        self.board_id = self.scope['url_route']['kwargs']['board_id']
        self.room_group_name = f"whiteboard_{self.board_id}"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Parse incoming WebSocket message
        data = json.loads(text_data)

        # Broadcast the data to all clients in the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "draw_event",
                "x1": data["x1"],
                "y1": data["y1"],
                "x2": data["x2"],
                "y2": data["y2"],
            }
        )

    async def draw_event(self, event):
        # Send the broadcasted data to WebSocket clients
        await self.send(text_data=json.dumps({
            "x1": event["x1"],
            "y1": event["y1"],
            "x2": event["x2"],
            "y2": event["y2"],
        }))
