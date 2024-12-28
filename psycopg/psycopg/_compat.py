"""
compatibility functions for different Python versions
"""

# Copyright (C) 2021 The Psycopg Team

import sys

from asyncio import to_thread
from zoneinfo import ZoneInfo
from functools import cache
from collections import Counter, deque as Deque


if sys.version_info >= (3, 10):
    from typing import TypeGuard, TypeAlias
else:
    from typing_extensions import TypeGuard, TypeAlias

if sys.version_info >= (3, 11):
    from typing import LiteralString, Self
else:
    from typing_extensions import LiteralString, Self

if sys.version_info >= (3, 13):
    from typing import TypeVar
else:
    from typing_extensions import TypeVar

__all__ = [
    "Counter",
    "Deque",
    "LiteralString",
    "Self",
    "TypeAlias",
    "TypeGuard",
    "TypeVar",
    "ZoneInfo",
    "cache",
    "to_thread",
]
