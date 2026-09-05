import asyncio
import json
import logging
import math
import random

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from . import state
logger = logging.getLogger(__name__)


class MonitorConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        role = self.scope.get("role")

        if not user or user.is_anonymous:
            logger.warning("WS connect rejected: no authenticated user")
            await self.close(code=4001)
            return

        self.group_name = f"monitor_{role}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        logger.info(
            "WS connected: user=%s role=%s group=%s",
            getattr(user, "email", user),
            role,
            self.group_name,
        )

        self._task = asyncio.ensure_future(self.stream_data())

    async def disconnect(self, close_code):
        logger.info("WS disconnecting: code=%s", close_code)

        if hasattr(self, "_task"):
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def stream_data(self):
        t = 0
        logger.debug("stream_data loop started")

        try:
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

                payload = {
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

                await self.send_json(payload)

                if t % 50 == 0:
                    logger.debug("stream_data tick=%s sent", t)

                t += 1
                await asyncio.sleep(0.2)

        except asyncio.CancelledError:
            logger.debug("stream_data loop cancelled")
            raise
        except Exception:
            logger.exception("stream_data loop crashed unexpectedly")
            raise