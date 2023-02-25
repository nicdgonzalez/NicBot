from __future__ import annotations

import asyncio
import json
import logging
import os
import typing

import discord
import discord.ext.commands

if typing.TYPE_CHECKING:
    from logging import Logger
    from typing import List

    from discord import ActivityType, Message
    from discord.ext.commands import Bot

# Relative to `../launcher.py`
RELATIVE_COGS_DIR_PATH: str = "./nicbot/cogs"


def get_config() -> dict:
    with open("./nicbot/config/config.json", "r") as f:
        config: dict = json.load(f)

    return config


class NicBot(discord.ext.commands.Bot):

    def __init__(self) -> None:
        self.config: dict = get_config()
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
        return None

    def __str__(self) -> str:
        return "%s - Discord Bot" % self.user.name

    async def on_ready(self) -> None:
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
    def get_custom_prefix(bot: Bot, message: Message) -> List[str]:
        base: List[str] = [f"<@!{bot.user.id}>", f"<@{bot.user.id}>"]
        base.append(bot.default_prefix)

        # Retrieve prefix from server and append to `base`
        # guild_id: int = message.guild.id

        return base

    def run(self) -> None:
        asyncio.run(self.load_cogs())
        return super().run(self.config.pop("token"))
