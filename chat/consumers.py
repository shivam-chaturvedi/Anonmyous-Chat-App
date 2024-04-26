from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async

import json
from urllib.parse import parse_qs
from chat.models import Member

class MyConsumer(AsyncConsumer):

    @database_sync_to_async
    def get_group(self,id):
        return Member.objects.get(id=id).Group

    async def websocket_connect(self,e):
        query_param=parse_qs(self.scope['query_string'].decode('utf-8'))
        id=int(query_param.get('id',[None])[0])
        print(id)

        print(self.channel_layer)
        print(self.channel_name)
        group=await self.get_group(id)
        print(group.id)
        self.group_name=str(group.id)
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        print(self.channel_layer.capacity)
        print("seding ...")
        await self.send({
            'type':'websocket.accept'
        })
        await self.send({
            'type':'websocket.send',
            'text':json.dumps({
                'members':[],
            })
        })

    async def websocket_receive(self,e):
        data=json.loads(e['text'])
        print(data)

        await self.channel_layer.group_send(self.group_name,{
            'type':'chat.message',
            'msg':e['text']
        })
        print(e)
        
    async def chat_message(self,e):
        message=e['msg']
        print(message)

        await self.send({
            'type':'websocket.send',
            'text':message
        })

    async def websocket_disconnect(self,e):
        print(e)
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        raise StopConsumer()