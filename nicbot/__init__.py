"""
NicBot
=======

A bot that runs on Discord, written in Python.
"""

__title__: str = "Templates"
__author__: str = "nicdgonzalez"
__license__: str = "Apache Software License"
__copyright__: str = f"Copyright (c) 2022-present {__author__}"
__version__: str = "0.1.0"
__repository__: str = ""

from typing import NamedTuple

from .bot import NicBot

class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int


version_info: VersionInfo = VersionInfo(*__version__.split(".", maxsplit=3))

del VersionInfo, NamedTuple
