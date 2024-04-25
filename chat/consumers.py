from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

class MyConsumer(AsyncConsumer):
    async def websocket_connect(self,e):
        print(e)
        print(self.channel_layer)
        print(self.channel_name)
        await self.channel_layer.group_add('p',self.channel_name)

        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self,e):
        await self.channel_layer.group_send('p',{
            'type':'chat.message',
            'msg':e['text']
        })
        print(e)
        
    async def chat_message(self,e):
        print(e)
        await self.send({
            'type':'websocket.send',
            'text':e['msg']
        })

    async def websocket_disconnect(self,e):
        print(e)
        raise StopConsumer()