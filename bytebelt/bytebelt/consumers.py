import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CodeSessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #recupère l'id du post dans l'url et crée un groupe de nom 'codesession_{post_id}'
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'codesession_{self.post_id}'

        #rejoint le groupe
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'code_change':
            code = data['code']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'code_message',
                    'code': code
                }
            )
        elif message_type == 'language_change':
            language = data['language']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'language_message',
                    'language': language
                }
            )

    async def code_message(self, event):
        code = event['code']
        await self.send(text_data=json.dumps({
            'type': 'code_change',
            'code': code
        }))

    async def language_message(self, event):
        language = event['language']
        await self.send(text_data=json.dumps({
            'type': 'language_change',
            'language': language
        }))
