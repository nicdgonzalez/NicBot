from __future__ import annotations

import typing

import discord.ext.commands

from .utils import add_cog

if typing.TYPE_CHECKING:
    from discord.ext.commands import Bot, Context


class Moderation(discord.ext.commands.Cog):

    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        return None

    @discord.ext.commands.Cog.listener()
    async def on_ready(self) -> None:
        """Runs once when the extension gets loaded."""

        self.bot.log.info('Loaded Cog: %s' % self.__class__.__name__)
        return None
    
    async def load(self, ctx: Context, name: str = None) -> None:
        return None
    
    async def unload(self, ctx: Context, name: str = None) -> None:
        return None
    
    async def reload(self, ctx: Context, name: str = None) -> None:
        return None


# Required at the end of every module
def setup(bot: Bot) -> None:
    return add_cog(bot, __name__)
