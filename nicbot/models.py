from __future__ import annotations

import json
import typing

import psycopg2

from . import pysql

if typing.TYPE_CHECKING:
    from .pysql import Column, Database

with open("./nicbot/config/config.json", "r") as f:
    config: dict = json.load(f)

dsn: str = pysql.DatabaseURI(**config.pop("database")).uri
db: Database = pysql.Database(
    psycopg2.connect,
    dsn=dsn
)


class Prefixes(db.Model, name="prefixes"):
    guild_id: Column = pysql.Column(pysql.Int8, not_null=True, unique=True)
    prefix: Column = pysql.Column(pysql.Text, not_null=True, default="$")


class RankSystem(db.Model, name="rank_system"):
    guild_id: Column = pysql.Column(pysql.Int8)
    user_id: Column = pysql.Column(pysql.Int8)
    level: Column = pysql.Column(pysql.Int8)
    experience: Column = pysql.Column(pysql.Int8)
    epoch: Column = pysql.Column(pysql.Int8)


# Create tables if they do not exist
Prefixes().create()
RankSystem().create()
