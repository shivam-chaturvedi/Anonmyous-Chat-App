from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async

import json
from urllib.parse import parse_qs
from chat.models import Member

class MyConsumer(AsyncConsumer):

    @database_sync_to_async
    def get_member_info(self,id):
        member=Member.objects.get(id=id)
        group = member.Group
       
        group_name = group.Name
        group_id = group.id
        group_members = [{'id':member.id,'name':member.Name} for member in group.member_set.all()] 

        return {'name':member.Name,'group_id':group_id,'group_name':group_name,'group_members':group_members}

    async def websocket_connect(self,e):
        query_param=parse_qs(self.scope['query_string'].decode('utf-8'))
        id=int(query_param.get('id',[None])[0])
        print(id)
        member_info=await self.get_member_info(1)
        print(member_info)
        self.group_id=str(member_info['group_id'])
        await self.channel_layer.group_add(self.group_id,self.channel_name)
        await self.send({
            'type':'websocket.accept'
        })
        await self.send({
            'type':'websocket.send',
            'text':json.dumps({
                'initialMessage':True,
                'members':member_info.get('group_members'),
                'groupName':member_info.get('group_name'),
                'groupId':member_info.get('group_id'),
                'username':member_info.get('name'),
            })
        })

    async def websocket_receive(self,e):
        data=json.loads(e['text'])
        data['initialMessage']=False
        member_info=await self.get_member_info(data['memberid'])
        print(member_info)
        data['name']=member_info.get('name')
        await self.channel_layer.group_send(self.group_id,{
            'type':'chat.message',
            'msg':json.dumps(data)
        })
        
    async def chat_message(self,e):
        message=e['msg']
        await self.send({
            'type':'websocket.send',
            'text':message,
        })

    async def websocket_disconnect(self,e):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        raise StopConsumer()