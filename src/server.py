from typing import TYPE_CHECKING

from fastapi import FastAPI

if TYPE_CHECKING:
    from bot import MonitoringBot

app = FastAPI()


@app.get("/status/{bot_id}")
async def get_bot_status(bot_id: int):
    bot: MonitoringBot = app.state.bot
    return bot.presences.get(bot_id, "unknown")
