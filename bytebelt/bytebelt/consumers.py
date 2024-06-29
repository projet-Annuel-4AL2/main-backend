import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CodeSessionConsumer(AsyncWebsocketConsumer):
    sessions = {}

    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'codesession_{self.post_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        session_state = self.sessions.get(self.post_id, {'code': '', 'language': 'javascript'})
        await self.send(text_data=json.dumps({
            'type': 'init',
            'code': session_state['code'],
            'language': session_state.get('language', 'javascript') 
        }))

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
            # save the code in the session state
            if self.post_id not in self.sessions:
                self.sessions[self.post_id] = {}
            self.sessions[self.post_id]['code'] = code

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'code_message',
                    'code': code
                }
            )
        elif message_type == 'language_change':
            language = data['language']
            # save the language in the session state
            if self.post_id not in self.sessions:
                self.sessions[self.post_id] = {}
            self.sessions[self.post_id]['language'] = language

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
