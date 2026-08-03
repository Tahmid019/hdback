import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from . import state

import math
import random


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
        
class MonitorConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
            user = self.scope.get("user")
            role = self.scope.get("role")

            if not user or user.is_anonymous:
                await self.close(code=4001)
                return

            self.group_name = f"monitor_{role}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
            if hasattr(self, 'group_name'):
                await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def stream_data(self):
        t = 0

        while True:
            heart_rate = random.randint(68, 75)
            spo2 = random.randint(97, 99)
            rr = random.randint(16, 20)
            removed = round(random.uniform(2.1, 2.45), 2)
            target = 2.50

            ecg_waveform = [
                round(math.sin((t + i) * 0.25) + random.uniform(-0.08, 0.08), 3)
                for i in range(120)
            ]

            respiration_waveform = [
                round(
                    0.8 * math.sin((t + i) * 0.06) + random.uniform(-0.03, 0.03),
                    3,
                )
                for i in range(120)
            ]

            await self.send_json(
                {
                    "source": "monitor",
                    "data": {
                        "ecg": {
                            "waveform": ecg_waveform,
                            "bpm": heart_rate,
                            "spo2": spo2,
                            "rr": rr,
                            "bp": {
                                "sys": random.randint(118, 124),
                                "dia": random.randint(76, 82),
                            },
                            "rhythm": "Normal Sinus Rhythm",
                            "lead": "Lead II",
                        },
                        "respiration": {
                            "waveform": respiration_waveform,
                            "rr": rr,
                            "pattern": "Normal",
                            "quality": "Good",
                        },
                        "vitals": {
                            "heart_rate": heart_rate,
                            "spo2": spo2,
                            "temperature": round(random.uniform(36.5, 37.1), 1),
                            "map": random.randint(88, 94),
                        },
                        "session": {
                            "total_fluid_removed": round(random.uniform(2.1, 2.5), 2),
                            "target_fluid": 2.5,

                            "ktv": round(random.uniform(1.05, 1.35), 2),
                            "ktv_target": 1.4,

                            "assigned_staff": [
                                {
                                    "id": "1",
                                    "initials": "AT",
                                },
                                {
                                    "id": "2",
                                    "initials": "RN",
                                },
                            ],
                        },
                        "fluid_balance": {
                            "removed": removed,
                            "target": target,
                            "remaining": round(target - removed, 2),
                            "unit": "L",
                            "status": "normal" if target - removed > 0.1 else "completed",
                        },
                    },
                }
            )

            t += 1
            await asyncio.sleep(0.2)