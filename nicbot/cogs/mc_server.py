from __future__ import annotations

import socket
import typing

import discord.ext.commands

from .utils import add_cog

if typing.TYPE_CHECKING:
    from socket import socket

    from discord.ext.commands import Bot, Context


class MinecraftServer(discord.ext.commands.Cog):
    """Stores commands and listeners related to our Minecraft server."""

    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.config: dict = self.bot.config.pop("mc_server")
        return None

    @discord.ext.commands.Cog.listener()
    async def on_ready(self) -> None:
        """Runs once when the extension gets loaded."""

        self.bot.log.info('Loaded Cog: %s' % self.__class__.__name__)
        return None

    @discord.ext.commands.command()
    async def status(self, ctx: Context) -> None:
        """Attempts to ping the Minecraft server to check if it is running.
        We assume the server is offline if the connection process times out.
        """

        status: bool = False
        server: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(5.0)

        await ctx.send("Pinging the Minecraft Server...")
        async with ctx.typing():
            try:
                server.connect((self.config["host"], self.config["port"]))
            except (TimeoutError,):
                pass  # The server is offline
            else:
                status |= True
                server.close()

        status: str = "Online" if status else "Offline"
        await ctx.channel.send(f"The Minecraft server is currently {status}.")
        return None


# Required at the end of every module.
def setup(bot: Bot) -> None:
    return add_cog(bot, __name__)
