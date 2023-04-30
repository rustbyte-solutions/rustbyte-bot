from typing import Any

import discord
from discord.ext import commands

from utils.bot import RustByteBot


class Admin(commands.Cog):
    def __init__(self, bot: RustByteBot) -> None:
        self.bot: RustByteBot = bot

    @commands.command()
    async def hello(self, ctx: commands.Context[Any]) -> None:
        embed = discord.Embed(title="Hello!", description="Hello world!")
        await ctx.reply(embed=embed)


async def setup(bot: RustByteBot) -> None:
    await bot.add_cog(Admin(bot))
