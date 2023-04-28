from __future__ import annotations

import datetime
import logging
import os
import pathlib
from typing import Any, Dict, List

import aiohttp
import asyncpg
import discord
from discord.ext import commands

class RustByteBot(commands.Bot):
    INITAL_EXTENSIONS: List[str] = []

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("rb!"),
            strip_after_prefix=True,
            allowed_mentions=discord.AllowedMentions(replied_user=False),
            case_insensitive=True,
            *args,
            **kwargs,
        )
        self.blacklisted_users: Dict[int, str] = {}
        self.cooldown: commands.CooldownMapping[discord.Message] = commands.CooldownMapping.from_cooldown(
            1, 1.5, commands.BucketType.member
        )
        self.maintenance: bool = False
        self.launch_time: datetime.datetime = datetime.datetime.utcnow()
    
    async def setup_hook(self) -> None:
        database: asyncpg.Pool[Any] | Any = await asyncpg.create_pool(
            host=os.environ["db_ip"],
            port=int(os.environ["db_port"]),
            user=os.environ["db_user"],
            password=os.environ["db_pwd"],
            database=os.environ["database"],
        )

        if not database:
            raise RuntimeError("Database is unreachable")
        else:
            self.database = database
        
        await self.load_extension("jishaku")
        for file in pathlib.Path("cogs").glob("**/*.py"):
            *tree, _ = file.parts
            if file.stem == "__init__":
                continue

            try:
                await self.load_extension(f"{".".join(tree)}.{file.stem}")
                self.INITAL_EXTENSIONS.append(f"{".".join(tree)}.{file.stem}")
            except Exception as error:
                self.logger.error(error, exc_info=error)

        try:
            log_webhook: str | None = os.environ["log_webhook"]
        except KeyError:
            raise RuntimeError("Logging Webhook isn't set in .env")

    async def close(self) -> None:
        if self.session:
            await self.session.close()

        if self.db:
            await self.db.close()

        await super().close()

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        discord.utils.setup_logging(handler=logging.FileHandler("bot.log"))
        self.logger: logging.Logger = logging.getLogger("discord")
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        await super().start(token)

    def get_log_webhook(self) -> discord.Webhook:
        return discord.Webhook.from_url(self.log_webhook, session=self.session, bot_token=os.getenv("token"))

    def is_blacklisted(self, user_id: int) -> bool:
        return user_id in self.blacklisted_users