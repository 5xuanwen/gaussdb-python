"""
Types used in the gaussdb_pool package
"""

# Copyright (C) 2023 The Psycopg Team

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Union
from collections.abc import Awaitable

from ._compat import TypeAlias, TypeVar

if TYPE_CHECKING:
    from typing import Any  # noqa: F401

    from gaussdb import AsyncConnection, Connection  # noqa: F401
    from gaussdb.rows import TupleRow  # noqa: F401

    from .pool import ConnectionPool  # noqa: F401
    from .pool_async import AsyncConnectionPool  # noqa: F401

# Connection types to make the pool generic
CT = TypeVar("CT", bound="Connection[Any]", default="Connection[TupleRow]")
ACT = TypeVar("ACT", bound="AsyncConnection[Any]", default="AsyncConnection[TupleRow]")

# Callbacks taking a connection from the pool
ConnectionCB: TypeAlias = Callable[[CT], None]
AsyncConnectionCB: TypeAlias = Callable[[ACT], Awaitable[None]]

# Callbacks to pass the pool to on connection failure
ConnectFailedCB: TypeAlias = Callable[["ConnectionPool[Any]"], None]
AsyncConnectFailedCB: TypeAlias = Union[
    Callable[["AsyncConnectionPool[Any]"], None],
    Callable[["AsyncConnectionPool[Any]"], Awaitable[None]],
]
