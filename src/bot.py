import logging
import os

import orjson
from discord import Client, Intents, MemberCacheFlags, Status

from config import monitor_ids

logger = logging.getLogger(__name__)


class MonitoringBot(Client):
    def __init__(self):
        # intents = Intents.all()
        intents = Intents(presences=True, members=True)
        self.presences: dict[int, str] = {}
        super().__init__(
            intents=intents,
            enable_debug_events=True,
            member_cache_flags=MemberCacheFlags.none(),
            chunk_guilds_at_startup=False,
            status=Status.invisible,
        )

    async def on_ready(self):
        logger.info("Bot ready!")  # TODO: fix this

        _common_guild = self.get_guild(int(os.environ["COMMON_GUILD_ID"]))
        if _common_guild is None:
            raise RuntimeError(f"The bot is not part of a guild with the ID {os.environ['COMMON_GUILD_ID']}")
        self.common_guild = _common_guild

        print("Bot ready !")

    async def on_socket_raw_receive(self, message: str):
        try:
            data = orjson.loads(message)
        except Exception:
            return

        if data["t"] != "PRESENCE_UPDATE":
            return

        user_id = int(data["d"]["user"]["id"])

        if user_id not in monitor_ids:
            return

        self.presences[user_id] = data["d"]["status"]
