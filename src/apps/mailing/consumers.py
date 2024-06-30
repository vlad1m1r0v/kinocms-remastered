import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MailingConsumer(AsyncWebsocketConsumer):
    async def celery_task_update(self, event):
        message = event["message"]
        await self.send(json.dumps(message))

    async def connect(self):
        await super().connect()
        task_id = self.scope.get("url_route").get("kwargs").get("task_id")
        await self.channel_layer.group_add(task_id, self.channel_name)

    async def disconnect(self, close_code):
        await self.close()
