import asyncio
import os

import discord
from dotenv import load_dotenv

load_dotenv()

from utils.bot import RustByteBot

bot = RustByteBot(intents=discord.Intents.all())


async def main() -> None:
    async with bot:
        await bot.start(os.environ["token"])


if __name__ == "__main__":
    asyncio.run(main())
