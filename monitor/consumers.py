import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . import state


class MonitorConsumer(AsyncWebsocketConsumer):
    GROUP = "monitor"

    # connect
    async def connect(self):
        await self.channel_layer.group_add(self.GROUP, self.channel_name)
        await self.accept()
        await self.send(json.dumps({"type": "snapshot", "data": state.get_state()}))
        self._task = asyncio.ensure_future(self._push_loop())

    # disconnect
    async def disconnect(self, code):
        self._task.cancel()
        await self.channel_layer.group_discard(self.GROUP, self.channel_name)

    # loop
    async def _push_loop(self):
        while True:
            await asyncio.sleep(0.04)
            chunk = await asyncio.to_thread(state.generate_wave_chunk)
            await self.send(json.dumps({"type": "wave", "data": chunk}))

    # broadcast
    async def monitor_broadcast(self, event):
        await self.send(json.dumps({"type": "update", "data": event["data"]}))
