# WARNING: this file is auto-generated by 'async_to_sync.py'
# from the original file '_copy_async.py'
# DO NOT CHANGE! Change the original file instead.
"""
Objects to support the COPY protocol (sync version).
"""

# Copyright (C) 2023 The Psycopg Team

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Iterator, Tuple, Sequence, TYPE_CHECKING

from . import pq
from . import errors as e
from ._compat import Self
from ._copy_base import BaseCopy, MAX_BUFFER_SIZE, QUEUE_SIZE, PREFER_FLUSH
from .generators import copy_to, copy_end
from ._encodings import pgconn_encoding
from ._acompat import spawn, gather, Queue, Worker

if TYPE_CHECKING:
    from .abc import Buffer
    from .cursor import Cursor
    from .connection import Connection  # noqa: F401

COPY_IN = pq.ExecStatus.COPY_IN
COPY_OUT = pq.ExecStatus.COPY_OUT

ACTIVE = pq.TransactionStatus.ACTIVE


class Copy(BaseCopy["Connection[Any]"]):
    """Manage an asynchronous :sql:`COPY` operation.

    :param cursor: the cursor where the operation is performed.
    :param binary: if `!True`, write binary format.
    :param writer: the object to write to destination. If not specified, write
        to the `!cursor` connection.

    Choosing `!binary` is not necessary if the cursor has executed a
    :sql:`COPY` operation, because the operation result describes the format
    too. The parameter is useful when a `!Copy` object is created manually and
    no operation is performed on the cursor, such as when using ``writer=``\\
    `~psycopg.copy.FileWriter`.
    """

    __module__ = "psycopg"

    writer: Writer

    def __init__(
        self,
        cursor: Cursor[Any],
        *,
        binary: bool | None = None,
        writer: Writer | None = None,
    ):
        super().__init__(cursor, binary=binary)
        if not writer:
            writer = LibpqWriter(cursor)

        self.writer = writer
        self._write = writer.write

    def __enter__(self) -> Self:
        self._enter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.finish(exc_val)

    # End user sync interface

    def __iter__(self) -> Iterator[Buffer]:
        """Implement block-by-block iteration on :sql:`COPY TO`."""
        while True:
            data = self.read()
            if not data:
                break
            yield data

    def read(self) -> Buffer:
        """
        Read an unparsed row after a :sql:`COPY TO` operation.

        Return an empty string when the data is finished.
        """
        return self.connection.wait(self._read_gen())

    def rows(self) -> Iterator[Tuple[Any, ...]]:
        """
        Iterate on the result of a :sql:`COPY TO` operation record by record.

        Note that the records returned will be tuples of unparsed strings or
        bytes, unless data types are specified using `set_types()`.
        """
        while True:
            record = self.read_row()
            if record is None:
                break
            yield record

    def read_row(self) -> Tuple[Any, ...] | None:
        """
        Read a parsed row of data from a table after a :sql:`COPY TO` operation.

        Return `!None` when the data is finished.

        Note that the records returned will be tuples of unparsed strings or
        bytes, unless data types are specified using `set_types()`.
        """
        return self.connection.wait(self._read_row_gen())

    def write(self, buffer: Buffer | str) -> None:
        """
        Write a block of data to a table after a :sql:`COPY FROM` operation.

        If the :sql:`COPY` is in binary format `!buffer` must be `!bytes`. In
        text mode it can be either `!bytes` or `!str`.
        """
        data = self.formatter.write(buffer)
        if data:
            self._write(data)

    def write_row(self, row: Sequence[Any]) -> None:
        """Write a record to a table after a :sql:`COPY FROM` operation."""
        data = self.formatter.write_row(row)
        if data:
            self._write(data)

    def finish(self, exc: BaseException | None) -> None:
        """Terminate the copy operation and free the resources allocated.

        You shouldn't need to call this function yourself: it is usually called
        by exit. It is available if, despite what is documented, you end up
        using the `Copy` object outside a block.
        """
        if self._direction == COPY_IN:
            data = self.formatter.end()
            if data:
                self._write(data)
            self.writer.finish(exc)
            self._finished = True
        else:
            if not exc:
                return
            if self._pgconn.transaction_status != ACTIVE:
                # The server has already finished to send copy data. The connection
                # is already in a good state.
                return
            # Throw a cancel to the server, then consume the rest of the copy data
            # (which might or might not have been already transferred entirely to
            # the client, so we won't necessary see the exception associated with
            # canceling).
            self.connection._try_cancel()
            self.connection.wait(self._end_copy_out_gen())


class Writer(ABC):
    """
    A class to write copy data somewhere (for async connections).
    """

    @abstractmethod
    def write(self, data: Buffer) -> None:
        """Write some data to destination."""
        ...

    def finish(self, exc: BaseException | None = None) -> None:
        """
        Called when write operations are finished.

        If operations finished with an error, it will be passed to ``exc``.
        """
        pass


class LibpqWriter(Writer):
    """
    An `Writer` to write copy data to a Postgres database.
    """

    __module__ = "psycopg.copy"

    def __init__(self, cursor: Cursor[Any]):
        self.cursor = cursor
        self.connection = cursor.connection
        self._pgconn = self.connection.pgconn

    def write(self, data: Buffer) -> None:
        if len(data) <= MAX_BUFFER_SIZE:
            # Most used path: we don't need to split the buffer in smaller
            # bits, so don't make a copy.
            self.connection.wait(copy_to(self._pgconn, data, flush=PREFER_FLUSH))
        else:
            # Copy a buffer too large in chunks to avoid causing a memory
            # error in the libpq, which may cause an infinite loop (#255).
            for i in range(0, len(data), MAX_BUFFER_SIZE):
                self.connection.wait(
                    copy_to(
                        self._pgconn, data[i : i + MAX_BUFFER_SIZE], flush=PREFER_FLUSH
                    )
                )

    def finish(self, exc: BaseException | None = None) -> None:
        bmsg: bytes | None
        if exc:
            msg = f"error from Python: {type(exc).__qualname__} - {exc}"
            bmsg = msg.encode(pgconn_encoding(self._pgconn), "replace")
        else:
            bmsg = None

        try:
            res = self.connection.wait(copy_end(self._pgconn, bmsg))
        # The QueryCanceled is expected if we sent an exception message to
        # pgconn.put_copy_end(). The Python exception that generated that
        # cancelling is more important, so don't clobber it.
        except e.QueryCanceled:
            if not bmsg:
                raise
        else:
            self.cursor._results = [res]


class QueuedLibpqWriter(LibpqWriter):
    """
    `Writer` using a buffer to queue data to write.

    `write()` returns immediately, so that the main thread can be CPU-bound
    formatting messages, while a worker thread can be IO-bound waiting to write
    on the connection.
    """

    __module__ = "psycopg.copy"

    def __init__(self, cursor: Cursor[Any]):
        super().__init__(cursor)

        self._queue: Queue[Buffer] = Queue(maxsize=QUEUE_SIZE)
        self._worker: Worker | None = None
        self._worker_error: BaseException | None = None

    def worker(self) -> None:
        """Push data to the server when available from the copy queue.

        Terminate reading when the queue receives a false-y value, or in case
        of error.

        The function is designed to be run in a separate task.
        """
        try:
            while True:
                data = self._queue.get()
                if not data:
                    break
                self.connection.wait(copy_to(self._pgconn, data, flush=PREFER_FLUSH))
        except BaseException as ex:
            # Propagate the error to the main thread.
            self._worker_error = ex

    def write(self, data: Buffer) -> None:
        if not self._worker:
            # warning: reference loop, broken by _write_end
            self._worker = spawn(self.worker)

        # If the worker thread raies an exception, re-raise it to the caller.
        if self._worker_error:
            raise self._worker_error

        if len(data) <= MAX_BUFFER_SIZE:
            # Most used path: we don't need to split the buffer in smaller
            # bits, so don't make a copy.
            self._queue.put(data)
        else:
            # Copy a buffer too large in chunks to avoid causing a memory
            # error in the libpq, which may cause an infinite loop (#255).
            for i in range(0, len(data), MAX_BUFFER_SIZE):
                self._queue.put(data[i : i + MAX_BUFFER_SIZE])

    def finish(self, exc: BaseException | None = None) -> None:
        self._queue.put(b"")

        if self._worker:
            gather(self._worker)
            self._worker = None  # break reference loops if any

        # Check if the worker thread raised any exception before terminating.
        if self._worker_error:
            raise self._worker_error

        super().finish(exc)
