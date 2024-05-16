from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async

import json
from urllib.parse import parse_qs
from ChatApp.models import Member,Groups

class MyConsumer(AsyncConsumer):

    @database_sync_to_async
    def delete_group(self,group_id):
        try:
            group=Groups.objects.get(id=group_id)
            group.delete()
            return "success"
        except Exception as e:
            return str(e)


    @database_sync_to_async
    def get_members(self,group_id):
        group=Groups.objects.get(id=group_id)
        group_members = [{'memberid':member.id,'name':member.Name} for member in group.member_set.all()] 
        return group_members
    
    @database_sync_to_async
    def delete_member(self,id):
        try:
            member=Member.objects.get(id=id)
            member.delete()
            return "success"
        except Exception as e:
            return str(e)

    @database_sync_to_async
    def get_member_info(self,id):
        try:
            member=Member.objects.get(id=id)
            group = member.Group
        
            group_name = group.Name
            group_id = group.id
            group_members = [{'memberid':member.id,'name':member.Name} for member in group.member_set.all()] 
    
            return {'group_id':group_id,'group_name':group_name,'group_members':group_members}
        except Exception as e:
            return {'error':str(e)}
        
    async def websocket_connect(self,e):
        await self.send({
                'type':'websocket.accept'
        })
        self.group_id=None
        query_param=parse_qs(self.scope['query_string'].decode('utf-8'))
        id=int(query_param.get('id',[None])[0])
       
        member_info=await self.get_member_info(id)
        if(member_info.get("error")):
            await self.send({
                "type":"websocket.send",
                'text':json.dumps({
                    "error":member_info.get("error")
                })
            })
            await self.send({
                "type":"websocket.close"
            })

        else:
            self.group_id=str(member_info['group_id'])
            await self.channel_layer.group_add(self.group_id,self.channel_name)
            
            await self.channel_layer.group_send(self.group_id,{
                'type':'chat.message',
                'msg':json.dumps({
                    'updateMemberInfo':True,
                    'members':member_info.get('group_members'),
                    'groupName':member_info.get('group_name'),
                    'groupId':member_info.get('group_id'),
                    
                })
            })

    async def websocket_receive(self,e):
        data=json.loads(e['text'])
        if(data.get("delete",None)):
            print("Delete request for member id",data.get("memberid"))
            member_info=await self.get_member_info(data.get("memberid"))
            res=await self.delete_member(data.get("memberid"))
            if(res=="success"):
                print("Member Deleted")
                self.group_id=str(member_info.get("group_id"))
                group_members_updated=await self.get_members(int(self.group_id))
                if(group_members_updated.__len__()==0):
                    # delete group also
                    await self.delete_group(int(self.group_id))

                await self.channel_layer.group_send(self.group_id,{
                    'type':'chat.message',
                    'msg':json.dumps({
                    'updateMemberInfo':True,
                    'members':group_members_updated,
                    'groupName':member_info.get('group_name'),
                    'groupId':member_info.get('group_id'),
                    
                })
                })

        else:
            data['updateMemberInfo']=False
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
        if(self.group_id):
            await self.channel_layer.group_discard(self.group_id,self.channel_name)
        raise StopConsumer()