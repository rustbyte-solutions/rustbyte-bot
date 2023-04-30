from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import discord
from discord import PartialEmoji
from discord.ext import commands
from typing_extensions import LiteralString, Self

if TYPE_CHECKING:
    from utils.bot import RustByteBot

BASE_KWARGS: dict[str, Any] = {
    "content": None,
    "embeds": [],
    "attachments": [],
    "suppress": False,
    "delete_after": None,
    "view": None,
}


class DeleteView(discord.ui.View):
    def __init__(self: Self, ctx: RustByteContext) -> None:
        super().__init__(timeout=None)
        self.ctx: RustByteContext = ctx

    @discord.ui.button(
        emoji="\U0001f5d1",
        style=discord.ButtonStyle.danger,
        label="Delete",
        custom_id="delete",
    )
    async def delete(self: Self, interaction: discord.Interaction, _) -> None:
        if interaction.user.id == self.ctx.author.id:
            if not interaction.message:
                return

            return await interaction.message.delete()

        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't delete it!",
            ephemeral=True,
        )


class _Emojis:
    x: PartialEmoji = PartialEmoji(name="cross", id=1019436205269602354)
    check: PartialEmoji = PartialEmoji(name="tick", id=1019436222260723744)
    slash: PartialEmoji = PartialEmoji(name="slash", id=1041021694682349569)


class RustByteContext(commands.Context["RustByteBot"]):
    Emojis: _Emojis = _Emojis()

    async def send(
        self: Self,
        content: str | None = None,
        add_button_view: bool = True,
        **kwargs: Any,
    ) -> discord.Message | Any:
        embed: Optional[discord.Embed] = kwargs.get("embed")
        if embed:
            if not embed.color:
                embed.color = discord.Color.random()

        if add_button_view:
            _view: discord.ui.View | None = kwargs.get("view")
            if not _view:
                kwargs["view"] = DeleteView(self)

            else:
                view = kwargs["view"] = DeleteView(self)
                view.add_item(_view.children[0])

        return await super().send(content, **kwargs)

    async def create_codeblock(self: Self, content: str) -> str:
        fmt: LiteralString = "`" * 3
        return f"{fmt}py\n{content}{fmt}"
