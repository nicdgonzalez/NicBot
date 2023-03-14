from __future__ import annotations

import math
import time
import typing

import discord
import discord.ext.commands

from .. import models
from .utils import add_cog

if typing.TYPE_CHECKING:
    from discord import User
    from discord.ext.commands import Bot, Context

    from ..pysql import Database

required_exp = lambda level: math.floor((level ** 3) + 12)
gained_exp = lambda level: math.ceil((((32 * level) * 1.25) / 7) + 1)
is_valid_level = lambda exp, level: (exp >= required_exp(level)) and (level <= 100)


class RankSystem(discord.ext.commands.Cog):

    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.db: Database = self.bot.db
        return None

    @discord.ext.commands.Cog.listener()
    async def on_ready(self) -> None:
        """Runs once when the extension gets loaded."""

        self.bot.log.info('Loaded Cog: %s' % self.__class__.__name__)
        return None

    def _get_user_data(self, guild_id: int, user_id: int) -> dict:
        result: tuple | None = self.db.query.fetch_one(
            models.RankSystem(guild_id=guild_id, user_id=user_id)
        )

        if bool(result):
            result = {
                "guild_id": guild_id,
                "user_id": user_id,
                "level": result[2],
                "experience": result[3],
                "epoch": result[4]
            }
        else:
            result = {
                "guild_id": guild_id,
                "user_id": user_id,
                "level": 1,
                "experience": 0,
                "epoch": time.time()
            }
            self.db.session.insert(models.RankSystem(**result))

        return result

    @discord.ext.commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if (message.author.bot):
            return

        guild_id, user_id = (message.guild.id, message.author.id)
        player_data: dict = self._get_user_data(guild_id, user_id)
        level: int = player_data["level"]
        experience: int = player_data["experience"]
        epoch: int = player_data["epoch"]

        if 0 <= (time.time() - epoch) < 60:
            return None  # There is a 60s cooldown between messages

        experience += gained_exp(level)

        has_leveled_up: bool = False
        while is_valid_level(experience, level):
            has_leveled_up |= True
            level += 1

        if has_leveled_up:
            experience *= 0
            await message.reply(f"Level up! You are now level {level}.")

        self.db.session.update(
            models.RankSystem(level=level, experience=experience, epoch=epoch),
            where={"guild_id": guild_id, "user_id": user_id}
        )

        return None

    @discord.ext.commands.is_owner()
    @discord.ext.commands.command()
    async def give_exp(self, ctx: Context, user: discord.User, amount: int) -> None:
        if (amount < 1):
            await ctx.reply("You can't give a negative amount... silly goose.")
            return None

        guild_id, user_id = (ctx.guild.id, user.id)
        player_data: dict = self._get_user_data(guild_id, user_id)

        level: int = player_data.get("level")
        experience: int = player_data.get("experience") + amount

        while is_valid_level(experience, level):
            level += 1

        self.db.session.update(
            models.RankSystem(
                level=level,
                experience=0
            ),
            where={"guild_id": guild_id, "user_id": user_id}
        )

        await ctx.reply(
            f"{user.mention} gained {experience} experience and is now level {level}."
        )

        return None

    @discord.ext.commands.command()
    async def reset_user(self, ctx: Context, user: discord.User) -> None:
        player_data: dict = self._get_user_data(ctx.guild.id, user.id)
        player_data.update(level=1, experience=0, epoch=0)

        self.db.session.update(
            models.RankSystem(**player_data),
            where={"guild_id": ctx.guild.id, "user_id": user.id}
        )
        await ctx.reply(f"{user.mention}'s stats have been reset.")

        return None


# Required at the end of every module
def setup(bot: Bot) -> None:
    return add_cog(bot, __name__)
