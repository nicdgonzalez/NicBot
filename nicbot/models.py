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
db: Database = pysql.Database(psycopg2.connect, dsn=dsn)


class Prefixes(db.Model, name="prefixes"):
    guild_id: Column = pysql.Column(pysql.Int8, not_null=True, unique=True)
    prefix: Column = pysql.Column(pysql.Text, not_null=True, default="$")


class RankSystem(db.Model, name="rank_system"):
    guild_id: Column = pysql.Column(pysql.Int8)
    user_id: Column = pysql.Column(pysql.Int8)
    level: Column = pysql.Column(pysql.Int8)
    experience: Column = pysql.Column(pysql.Int8)
    epoch: Column = pysql.Column(pysql.Int8)


class RankRoles(db.Model, name="rank_roles"):
    guild_id: Column = pysql.Column(
        pysql.Int8,
        foreign_key=pysql.ForeignKey(RankSystem.guild_id)
    )
    rank_1_role: Column = pysql.Column(pysql.Int8)
    rank_1_level: Column = pysql.Column(pysql.Int8)
    rank_2_role: Column = pysql.Column(pysql.Int8)
    rank_2_level: Column = pysql.Column(pysql.Int8)
    rank_3_role: Column = pysql.Column(pysql.Int8)
    rank_3_level: Column = pysql.Column(pysql.Int8)
    rank_4_role: Column = pysql.Column(pysql.Int8)
    rank_4_level: Column = pysql.Column(pysql.Int8)
    rank_5_role: Column = pysql.Column(pysql.Int8)
    rank_5_level: Column = pysql.Column(pysql.Int8)
    rank_6_role: Column = pysql.Column(pysql.Int8)
    rank_6_level: Column = pysql.Column(pysql.Int8)
    rank_7_role: Column = pysql.Column(pysql.Int8)
    rank_7_level: Column = pysql.Column(pysql.Int8)
    rank_8_role: Column = pysql.Column(pysql.Int8)
    rank_8_level: Column = pysql.Column(pysql.Int8)
    rank_9_role: Column = pysql.Column(pysql.Int8)
    rank_9_level: Column = pysql.Column(pysql.Int8)


# Create tables if they do not exist
Prefixes().create()
RankSystem().create()
