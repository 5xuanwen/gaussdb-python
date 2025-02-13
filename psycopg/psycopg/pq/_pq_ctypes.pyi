"""
types stub for ctypes functions
"""

# Copyright (C) 2020 The Psycopg Team

from ctypes import Array, _Pointer, c_char, c_char_p, c_int, c_ubyte, c_uint, c_ulong
from ctypes import pointer
from typing import Any, Callable, Sequence

class FILE: ...

def fdopen(fd: int, mode: bytes) -> _Pointer[FILE]: ...  # type: ignore[type-var]

Oid = c_uint

class PGconn_struct: ...
class PGresult_struct: ...
class PGcancelConn_struct: ...
class PGcancel_struct: ...

class PQconninfoOption_struct:
    keyword: bytes
    envvar: bytes
    compiled: bytes
    val: bytes
    label: bytes
    dispchar: bytes
    dispsize: int

class PGnotify_struct:
    be_pid: int
    relname: bytes
    extra: bytes

class PGresAttDesc_struct:
    name: bytes
    tableid: int
    columnid: int
    format: int
    typid: int
    typlen: int
    atttypmod: int

def PQhostaddr(arg1: PGconn_struct | None) -> bytes: ...
def PQerrorMessage(arg1: PGconn_struct | None) -> bytes: ...
def PQresultErrorMessage(arg1: PGresult_struct | None) -> bytes: ...
def PQexecPrepared(
    arg1: PGconn_struct | None,
    arg2: bytes,
    arg3: int,
    arg4: Array[c_char_p] | None,
    arg5: Array[c_int] | None,
    arg6: Array[c_int] | None,
    arg7: int,
) -> PGresult_struct: ...
def PQprepare(
    arg1: PGconn_struct | None,
    arg2: bytes,
    arg3: bytes,
    arg4: int,
    arg5: Array[c_uint] | None,
) -> PGresult_struct: ...
def PQgetvalue(
    arg1: PGresult_struct | None, arg2: int, arg3: int
) -> _Pointer[c_char]: ...
def PQcmdTuples(arg1: PGresult_struct | None) -> bytes: ...
def PQescapeStringConn(
    arg1: PGconn_struct | None,
    arg2: c_char_p,
    arg3: bytes,
    arg4: int,
    arg5: _Pointer[c_int],
) -> int: ...
def PQescapeString(arg1: c_char_p, arg2: bytes, arg3: int) -> int: ...
def PQsendPrepare(
    arg1: PGconn_struct | None,
    arg2: bytes,
    arg3: bytes,
    arg4: int,
    arg5: Array[c_uint] | None,
) -> int: ...
def PQsendQueryPrepared(
    arg1: PGconn_struct | None,
    arg2: bytes,
    arg3: int,
    arg4: Array[c_char_p] | None,
    arg5: Array[c_int] | None,
    arg6: Array[c_int] | None,
    arg7: int,
) -> int: ...
def PQcancelCreate(arg1: PGconn_struct | None) -> PGcancelConn_struct: ...
def PQcancelBlocking(arg1: PGcancelConn_struct | None) -> int: ...
def PQcancelStart(arg1: PGcancelConn_struct | None) -> int: ...
def PQcancelPoll(arg1: PGcancelConn_struct | None) -> int: ...
def PQcancelStatus(arg1: PGcancelConn_struct | None) -> int: ...
def PQcancelSocket(arg1: PGcancelConn_struct | None) -> int: ...
def PQcancelErrorMessage(arg1: PGcancelConn_struct | None) -> bytes: ...
def PQcancelReset(arg1: PGcancelConn_struct | None) -> None: ...
def PQcancelFinish(arg1: PGcancelConn_struct | None) -> None: ...
def PQcancel(arg1: PGcancel_struct | None, arg2: c_char_p, arg3: int) -> int: ...
def PQsetNoticeReceiver(
    arg1: PGconn_struct, arg2: Callable[[Any], PGresult_struct], arg3: Any
) -> Callable[[Any], PGresult_struct]: ...

# TODO: Ignoring type as getting an error on mypy/ctypes:
# Type argument "psycopg.pq._pq_ctypes.PGnotify_struct" of "pointer" must be
# a subtype of "ctypes._CData"
def PQnotifies(
    arg1: PGconn_struct | None,
) -> _Pointer[PGnotify_struct] | None: ...  # type: ignore
def PQputCopyEnd(arg1: PGconn_struct | None, arg2: bytes | None) -> int: ...

# Arg 2 is a _Pointer, reported as _CArgObject by mypy
def PQgetCopyData(arg1: PGconn_struct | None, arg2: Any, arg3: int) -> int: ...
def PQsetResultAttrs(
    arg1: PGresult_struct | None,
    arg2: int,
    arg3: Array[PGresAttDesc_struct],  # type: ignore
) -> int: ...
def PQtrace(
    arg1: PGconn_struct | None,
    arg2: _Pointer[FILE],  # type: ignore[type-var]
) -> None: ...
def PQsetTraceFlags(arg1: PGconn_struct | None, arg2: int) -> None: ...
def PQencryptPasswordConn(
    arg1: PGconn_struct | None,
    arg2: bytes,
    arg3: bytes,
    arg4: bytes | None,
) -> bytes: ...
def PQpipelineStatus(pgconn: PGconn_struct | None) -> int: ...
def PQenterPipelineMode(pgconn: PGconn_struct | None) -> int: ...
def PQexitPipelineMode(pgconn: PGconn_struct | None) -> int: ...
def PQpipelineSync(pgconn: PGconn_struct | None) -> int: ...
def PQsendFlushRequest(pgconn: PGconn_struct | None) -> int: ...

# Autogenerated section.
# In order to refresh, run:
#   python -m psycopg.pq._pq_ctypes

# fmt: off
# autogenerated: start
def PQlibVersion() -> int: ...
def PQconnectdb(arg1: bytes) -> PGconn_struct: ...
def PQconnectStart(arg1: bytes) -> PGconn_struct: ...
def PQconnectPoll(arg1: PGconn_struct | None) -> int: ...
def PQconndefaults() -> Sequence[PQconninfoOption_struct]: ...
def PQconninfoFree(arg1: Sequence[PQconninfoOption_struct]) -> None: ...
def PQconninfo(arg1: PGconn_struct | None) -> Sequence[PQconninfoOption_struct]: ...
def PQconninfoParse(arg1: bytes, arg2: _Pointer[c_char_p]) -> Sequence[PQconninfoOption_struct]: ...
def PQfinish(arg1: PGconn_struct | None) -> None: ...
def PQreset(arg1: PGconn_struct | None) -> None: ...
def PQresetStart(arg1: PGconn_struct | None) -> int: ...
def PQresetPoll(arg1: PGconn_struct | None) -> int: ...
def PQping(arg1: bytes) -> int: ...
def PQdb(arg1: PGconn_struct | None) -> bytes | None: ...
def PQuser(arg1: PGconn_struct | None) -> bytes | None: ...
def PQpass(arg1: PGconn_struct | None) -> bytes | None: ...
def PQhost(arg1: PGconn_struct | None) -> bytes | None: ...
def PQport(arg1: PGconn_struct | None) -> bytes | None: ...
def PQtty(arg1: PGconn_struct | None) -> bytes | None: ...
def PQoptions(arg1: PGconn_struct | None) -> bytes | None: ...
def PQstatus(arg1: PGconn_struct | None) -> int: ...
def PQtransactionStatus(arg1: PGconn_struct | None) -> int: ...
def PQparameterStatus(arg1: PGconn_struct | None, arg2: bytes) -> bytes | None: ...
def PQprotocolVersion(arg1: PGconn_struct | None) -> int: ...
def PQserverVersion(arg1: PGconn_struct | None) -> int: ...
def PQsocket(arg1: PGconn_struct | None) -> int: ...
def PQbackendPID(arg1: PGconn_struct | None) -> int: ...
def PQconnectionNeedsPassword(arg1: PGconn_struct | None) -> int: ...
def PQconnectionUsedPassword(arg1: PGconn_struct | None) -> int: ...
def PQsslInUse(arg1: PGconn_struct | None) -> int: ...
def PQexec(arg1: PGconn_struct | None, arg2: bytes) -> PGresult_struct: ...
def PQexecParams(arg1: PGconn_struct | None, arg2: bytes, arg3: int, arg4: _Pointer[c_uint], arg5: _Pointer[c_char_p], arg6: _Pointer[c_int], arg7: _Pointer[c_int], arg8: int) -> PGresult_struct: ...
def PQdescribePrepared(arg1: PGconn_struct | None, arg2: bytes) -> PGresult_struct: ...
def PQdescribePortal(arg1: PGconn_struct | None, arg2: bytes) -> PGresult_struct: ...
def PQclosePrepared(arg1: PGconn_struct | None, arg2: bytes) -> PGresult_struct: ...
def PQclosePortal(arg1: PGconn_struct | None, arg2: bytes) -> PGresult_struct: ...
def PQresultStatus(arg1: PGresult_struct | None) -> int: ...
def PQresultErrorField(arg1: PGresult_struct | None, arg2: int) -> bytes | None: ...
def PQclear(arg1: PGresult_struct | None) -> None: ...
def PQntuples(arg1: PGresult_struct | None) -> int: ...
def PQnfields(arg1: PGresult_struct | None) -> int: ...
def PQfname(arg1: PGresult_struct | None, arg2: int) -> bytes | None: ...
def PQftable(arg1: PGresult_struct | None, arg2: int) -> int: ...
def PQftablecol(arg1: PGresult_struct | None, arg2: int) -> int: ...
def PQfformat(arg1: PGresult_struct | None, arg2: int) -> int: ...
def PQftype(arg1: PGresult_struct | None, arg2: int) -> int: ...
def PQfmod(arg1: PGresult_struct | None, arg2: int) -> int: ...
def PQfsize(arg1: PGresult_struct | None, arg2: int) -> int: ...
def PQbinaryTuples(arg1: PGresult_struct | None) -> int: ...
def PQgetisnull(arg1: PGresult_struct | None, arg2: int, arg3: int) -> int: ...
def PQgetlength(arg1: PGresult_struct | None, arg2: int, arg3: int) -> int: ...
def PQnparams(arg1: PGresult_struct | None) -> int: ...
def PQparamtype(arg1: PGresult_struct | None, arg2: int) -> int: ...
def PQcmdStatus(arg1: PGresult_struct | None) -> bytes | None: ...
def PQoidValue(arg1: PGresult_struct | None) -> int: ...
def PQescapeLiteral(arg1: PGconn_struct | None, arg2: bytes, arg3: int) -> bytes | None: ...
def PQescapeIdentifier(arg1: PGconn_struct | None, arg2: bytes, arg3: int) -> bytes | None: ...
def PQescapeByteaConn(arg1: PGconn_struct | None, arg2: bytes, arg3: int, arg4: _Pointer[c_ulong]) -> _Pointer[c_ubyte]: ...
def PQescapeBytea(arg1: bytes, arg2: int, arg3: _Pointer[c_ulong]) -> _Pointer[c_ubyte]: ...
def PQunescapeBytea(arg1: bytes, arg2: _Pointer[c_ulong]) -> _Pointer[c_ubyte]: ...
def PQsendQuery(arg1: PGconn_struct | None, arg2: bytes) -> int: ...
def PQsendQueryParams(arg1: PGconn_struct | None, arg2: bytes, arg3: int, arg4: _Pointer[c_uint], arg5: _Pointer[c_char_p], arg6: _Pointer[c_int], arg7: _Pointer[c_int], arg8: int) -> int: ...
def PQsendDescribePrepared(arg1: PGconn_struct | None, arg2: bytes) -> int: ...
def PQsendDescribePortal(arg1: PGconn_struct | None, arg2: bytes) -> int: ...
def PQsendClosePrepared(arg1: PGconn_struct | None, arg2: bytes) -> int: ...
def PQsendClosePortal(arg1: PGconn_struct | None, arg2: bytes) -> int: ...
def PQgetResult(arg1: PGconn_struct | None) -> PGresult_struct: ...
def PQconsumeInput(arg1: PGconn_struct | None) -> int: ...
def PQisBusy(arg1: PGconn_struct | None) -> int: ...
def PQsetnonblocking(arg1: PGconn_struct | None, arg2: int) -> int: ...
def PQisnonblocking(arg1: PGconn_struct | None) -> int: ...
def PQflush(arg1: PGconn_struct | None) -> int: ...
def PQsetSingleRowMode(arg1: PGconn_struct | None) -> int: ...
def PQsetChunkedRowsMode(arg1: PGconn_struct | None, arg2: int) -> int: ...
def PQgetCancel(arg1: PGconn_struct | None) -> PGcancel_struct: ...
def PQfreeCancel(arg1: PGcancel_struct | None) -> None: ...
def PQputCopyData(arg1: PGconn_struct | None, arg2: bytes, arg3: int) -> int: ...
def PQuntrace(arg1: PGconn_struct | None) -> None: ...
def PQfreemem(arg1: Any) -> None: ...
def PQchangePassword(arg1: PGconn_struct | None, arg2: bytes, arg3: bytes) -> PGresult_struct: ...
def PQmakeEmptyPGresult(arg1: PGconn_struct | None, arg2: int) -> PGresult_struct: ...
def PQinitOpenSSL(arg1: int, arg2: int) -> None: ...
# autogenerated: end
# fmt: on
