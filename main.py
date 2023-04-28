import discord
import asyncio
from utils import RustByteBot

bot = RustByteBot(intents=discord.Intents.all())

async def main() -> None:
    async with bot:
        await bot.start(os.environ["token"])


if __name__ == "__main__":
    asyncio.run(main())