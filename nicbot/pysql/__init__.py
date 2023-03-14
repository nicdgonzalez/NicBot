"""
PySQL
======

**PySQL** is an an object-relational mapper (ORM) for SQL databases.
"""

__title__: str = "PySQL"
__author__: str = "nicdgonzalez"
__license__: str = "Apache Software License"
__copyright__: str = f"Copyright (c) 2022-present {__author__}"
__version__: str = "0.1.0"

from typing import NamedTuple

from .column import *
from .constraints import *
from .core import *
from .errors import *
from .model import *
from .query import *
from .schema import *
from .session import *
from .statement import *
from .table import *
from .types import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int


version_info: VersionInfo = VersionInfo(*__version__.split(".", maxsplit=3))

del NamedTuple, VersionInfo
