from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List

__all__: List[str] = [
    "PySQLException",
    "MissingSchemaNameError"
]


class PySQLException(Exception):
    pass


class MissingSchemaNameError(PySQLException):
    pass
