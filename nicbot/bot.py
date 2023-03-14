from __future__ import annotations

import asyncio
import json
import logging
import os
import typing

import discord
import discord.ext.commands

from .models import Prefixes, db

if typing.TYPE_CHECKING:
    from logging import Logger
    from typing import List

    from discord import ActivityType, Message

    from .pysql import Database

# Relative to `../launcher.py`
RELATIVE_COGS_DIR_PATH: str = "./nicbot/cogs"

user_id: int = None
prefix_base: List[str] = None
prefix_cache: dict = {}


class NicBot(discord.ext.commands.Bot):
    """Represents a bot that runs on Discord."""

    def __init__(self) -> None:
        with open("./nicbot/config/config.json", "r") as f:
            self.config: dict = json.load(f)

        self.default_prefix: str = self.config.pop("default_prefix")
        super().__init__(
            command_prefix=self.get_custom_prefix,
            help_command=None,
            case_insensitive=self.config.pop("case_insensitive"),
            description=self.config.pop("description"),
            self_bot= self.config.pop("self_bot"),
            owner_id=int(self.config.pop("owner_id")),
            owner_ids=set(self.config.pop("owner_ids")),
            strip_after_prefix=self.config.pop("strip_after_prefix"),
            intents=discord.Intents.all()
        )
        self.log: Logger = logging.getLogger(__name__)
        self.db: Database = db

        return None

    def __str__(self) -> str:
        return "%s - Discord Bot" % self.user.name

    async def on_ready(self) -> None:
        """Runs once when the bot officially displays online on Discord."""

        self.log.info(f"{self.user} ({self.user.id}) is now Online!")

        activity_type: ActivityType = discord.ActivityType.watching
        await self.change_presence(
            activity=discord.Activity(
                type=activity_type,
                name=f"{self.default_prefix}help"
            ),
            status=discord.Status.online
        )

        return None

    async def load_cogs(self) -> None:
        """Automatically fetches and loads all valid extensions from
        the '/cogs' directory. Automatically skipped are any modules with one
        or more leading underscores.
        """

        cogs: List[str] = [
            ext for ext
            in os.listdir(RELATIVE_COGS_DIR_PATH)
            if not ext.startswith("_")
            and ext.endswith(".py")
        ]

        for cog in cogs:
            dot_format: str = (
                RELATIVE_COGS_DIR_PATH
                .replace("\\", "/")
                .replace("/", ".")
                .strip(".")
                + "."
            )
            name: str = dot_format + cog[:-3]
            await self.load_extension(name=name, package=None)

        return None

    @staticmethod
    def get_custom_prefix(bot: "NicBot", message: Message, /) -> List[str]:
        """Gets a list of available prefixes the bot will respond to."""

        global prefix_base, prefix_cache, user_id

        if not bool(user_id):
            user_id = bot.user.id

        if not bool(prefix_base):
            prefix_base = [f"<@!{user_id}>", f"<@{user_id}>"]


        guild_id: int = message.guild.id
        prefix = prefix_cache.get(guild_id, None)

        if bool(prefix):
            return prefix_base + list(prefix)

        entry: Prefixes = Prefixes(guild_id=guild_id)
        prefix: str = bot.db.query.fetch_one(entry, select=["prefix"])

        if not bool(prefix):
            bot.db.session.insert(entry)
            prefix = bot.default_prefix
        else:
            prefix = prefix[0]

        prefix_cache[guild_id] = prefix

        return prefix_base + list(prefix)

    def run(self) -> None:
        """Starts the bot. This function is blocking and will not return until
        the bot has disconnected.
        """

        asyncio.run(self.load_cogs())
        return super().run(self.config.pop("token"))
