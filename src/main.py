import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from bot import MonitoringBot
from server import app

if "TOKEN" not in os.environ:
    raise RuntimeError("The environ variable TOKEN must be defined.")


async def bot_runner(bot: MonitoringBot):
    async with bot:
        await bot.start(os.environ["TOKEN"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    bot = MonitoringBot()
    app.state.bot = bot

    task = asyncio.create_task(bot_runner(bot))
    task.add_done_callback(lambda t: t.result())

    yield

    await bot.close()
    await task


app.router.lifespan_context = lifespan
