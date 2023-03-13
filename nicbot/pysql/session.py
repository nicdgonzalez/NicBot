from __future__ import annotations

from typing import TYPE_CHECKING

from .model import Model
from .statement import Statement
from .table import Table

if TYPE_CHECKING:
    from typing import Any, Dict, List, Union

    from .core import Database

__all__: List[str] = [
    "Session"
]


class Session:

    def __init__(self, __db: Database, /) -> None:
        self.db: Database = __db
        return None

    def insert(self, __t: Union[Table, Model], /) -> None:
        model: Model = __t if isinstance(__t, Model) else __t.to_model()
        table_name: str = model.table.name
        column_names: List[str] = list(model.kwargs.keys())
        values: List[Any] = list(model.kwargs.values())
        columns: str = ", ".join(column_names)
        placeholders: str = ", ".join([
            self.db.placeholder for _ in range(len(column_names))
        ])
        return self.db._execute(Statement(
            f'INSERT INTO {table_name}({columns}) VALUES({placeholders})',
            tuple(values)
        ))

    def update(
        self,
        __t: Union[Table, Model],
        /,
        where: Dict[str, Any] = {}
    ) -> None:
        model: Model = __t if isinstance(__t, Model) else __t.to_model()
        table_name: str = model.table.name
        placeholder: str = self.db.placeholder
        
        updates: str = ", ".join([
            f"{name} = {placeholder}" for (name)
            in model.kwargs.keys()
        ])
        values: List[Any] = list(model.kwargs.values())

        sql: str = f'UPDATE {table_name} SET {updates}'

        if (bool(where)):
            base_where: str = "WHERE "
            for (name, value) in where.items():
                base_where += f"{name} = {placeholder} AND "
                values.append(value)
            sql += " " + base_where.strip("AND ")

        return self.db._execute(Statement(sql, tuple(values)))

    def delete(self, __t: Union[Table, Model], /) -> None:
        model: Model = __t if isinstance(__t, Model) else __t.to_model()
        table_name: str = model.table.name
        placeholder: str = self.db.placeholder

        sql: str = f'DELETE FROM {table_name}'
        values: List[Any] = []

        if (where := model.kwargs):
            base_where: str = "WHERE "
            for (name, value) in where.items():
                base_where += f"{name} = {placeholder} AND "
                values.append(value)
            sql += " " + base_where.strip("AND ")

        return self.db._execute(Statement(sql, tuple(values)))
