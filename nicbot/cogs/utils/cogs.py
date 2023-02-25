from __future__ import annotations

import inspect
import sys
import typing

import discord.ext.commands

if typing.TYPE_CHECKING:
    from typing import List

    from discord.ext.commands import Bot


async def add_cog(bot: Bot, name: str) -> None:
    """This is a dynamic version of the `setup` function required at the end
    of all extented modules. This function will automatically gather all
    the classes in the module and run the `bot.add_cog` function to any
    that subclass `.Cog` from the 'discord.py' library.

    Usage
    ------
    ```python
    def setup(bot):
        add_cog(bot, __name__)
    ```
    """

    cogs: List[str] = [
        obj
        for _, obj
        in inspect.getmembers(sys.modules[name], inspect.isclass)
    ]

    for cog in cogs:
        if issubclass(cog, discord.ext.commands.Cog):
            await bot.add_cog(cog(bot))

    return None
