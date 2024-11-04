import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatRoom, Message, Contact, Conversation

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        # Save the message to the database
        await self.create_message({
            'room_name': self.room_name,
            'sender': sender,
            'message': message
        })

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async
    def create_message(self, data):
        room = ChatRoom.objects.get(name=data['room_name'])
        sender = Contact.objects.get(user__username=data['sender'])
        # Create a new Conversation if one doesn't exist
        conversation, created = Conversation.objects.get_or_create(chat_room=room)
        if created:
            conversation.participants.add(sender)

        Message.objects.create(conversation=conversation, sender=sender, message=data['message'])
