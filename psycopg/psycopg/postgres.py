"""
Types configuration specific to PostgreSQL.
"""

# Copyright (C) 2020 The Psycopg Team

from .abc import AdaptContext
from ._typemod import BitTypeModifier, CharTypeModifier, NumericTypeModifier
from ._typemod import TimeTypeModifier
from ._typeinfo import TypeInfo, TypesRegistry
from ._adapters_map import AdaptersMap

# Global objects with PostgreSQL builtins and globally registered user types.
types = TypesRegistry()

# Global adapter maps with PostgreSQL types configuration
adapters = AdaptersMap(types=types)


def register_default_types(types: TypesRegistry) -> None:
    from .types.range import RangeInfo
    from .types.multirange import MultirangeInfo

    # Use tools/update_oids.py to update this data.
    for t in [
        TypeInfo('"char"', 18, 1002, typemod=CharTypeModifier),
        # autogenerated: start
        # Generated from PostgreSQL 17.0
        TypeInfo("aclitem", 1033, 1034),
        TypeInfo("bit", 1560, 1561, typemod=BitTypeModifier),
        TypeInfo("bool", 16, 1000, regtype="boolean"),
        TypeInfo("box", 603, 1020, delimiter=";"),
        TypeInfo("bpchar", 1042, 1014, regtype="character", typemod=CharTypeModifier),
        TypeInfo("bytea", 17, 1001),
        TypeInfo("cid", 29, 1012),
        TypeInfo("cidr", 650, 651),
        TypeInfo("circle", 718, 719),
        TypeInfo("date", 1082, 1182),
        TypeInfo("float4", 700, 1021, regtype="real"),
        TypeInfo("float8", 701, 1022, regtype="double precision"),
        TypeInfo("gtsvector", 3642, 3644),
        TypeInfo("inet", 869, 1041),
        TypeInfo("int2", 21, 1005, regtype="smallint"),
        TypeInfo("int2vector", 22, 1006),
        TypeInfo("int4", 23, 1007, regtype="integer"),
        TypeInfo("int8", 20, 1016, regtype="bigint"),
        TypeInfo("interval", 1186, 1187, typemod=TimeTypeModifier),
        TypeInfo("json", 114, 199),
        TypeInfo("jsonb", 3802, 3807),
        TypeInfo("jsonpath", 4072, 4073),
        TypeInfo("line", 628, 629),
        TypeInfo("lseg", 601, 1018),
        TypeInfo("macaddr", 829, 1040),
        TypeInfo("macaddr8", 774, 775),
        TypeInfo("money", 790, 791),
        TypeInfo("name", 19, 1003),
        TypeInfo("numeric", 1700, 1231, typemod=NumericTypeModifier),
        TypeInfo("oid", 26, 1028),
        TypeInfo("oidvector", 30, 1013),
        TypeInfo("path", 602, 1019),
        TypeInfo("pg_lsn", 3220, 3221),
        TypeInfo("point", 600, 1017),
        TypeInfo("polygon", 604, 1027),
        TypeInfo("record", 2249, 2287),
        TypeInfo("refcursor", 1790, 2201),
        TypeInfo("regclass", 2205, 2210),
        TypeInfo("regcollation", 4191, 4192),
        TypeInfo("regconfig", 3734, 3735),
        TypeInfo("regdictionary", 3769, 3770),
        TypeInfo("regnamespace", 4089, 4090),
        TypeInfo("regoper", 2203, 2208),
        TypeInfo("regoperator", 2204, 2209),
        TypeInfo("regproc", 24, 1008),
        TypeInfo("regprocedure", 2202, 2207),
        TypeInfo("regrole", 4096, 4097),
        TypeInfo("regtype", 2206, 2211),
        TypeInfo("text", 25, 1009),
        TypeInfo("tid", 27, 1010),
        TypeInfo(
            "time",
            1083,
            1183,
            regtype="time without time zone",
            typemod=TimeTypeModifier,
        ),
        TypeInfo(
            "timestamp",
            1114,
            1115,
            regtype="timestamp without time zone",
            typemod=TimeTypeModifier,
        ),
        TypeInfo(
            "timestamptz",
            1184,
            1185,
            regtype="timestamp with time zone",
            typemod=TimeTypeModifier,
        ),
        TypeInfo(
            "timetz",
            1266,
            1270,
            regtype="time with time zone",
            typemod=TimeTypeModifier,
        ),
        TypeInfo("tsquery", 3615, 3645),
        TypeInfo("tsvector", 3614, 3643),
        TypeInfo("txid_snapshot", 2970, 2949),
        TypeInfo("uuid", 2950, 2951),
        TypeInfo("varbit", 1562, 1563, regtype="bit varying", typemod=BitTypeModifier),
        TypeInfo(
            "varchar", 1043, 1015, regtype="character varying", typemod=CharTypeModifier
        ),
        TypeInfo("xid", 28, 1011),
        TypeInfo("xid8", 5069, 271),
        TypeInfo("xml", 142, 143),
        RangeInfo("daterange", 3912, 3913, subtype_oid=1082),
        RangeInfo("int4range", 3904, 3905, subtype_oid=23),
        RangeInfo("int8range", 3926, 3927, subtype_oid=20),
        RangeInfo("numrange", 3906, 3907, subtype_oid=1700),
        RangeInfo("tsrange", 3908, 3909, subtype_oid=1114),
        RangeInfo("tstzrange", 3910, 3911, subtype_oid=1184),
        MultirangeInfo("datemultirange", 4535, 6155, range_oid=3912, subtype_oid=1082),
        MultirangeInfo("int4multirange", 4451, 6150, range_oid=3904, subtype_oid=23),
        MultirangeInfo("int8multirange", 4536, 6157, range_oid=3926, subtype_oid=20),
        MultirangeInfo("nummultirange", 4532, 6151, range_oid=3906, subtype_oid=1700),
        MultirangeInfo("tsmultirange", 4533, 6152, range_oid=3908, subtype_oid=1114),
        MultirangeInfo("tstzmultirange", 4534, 6153, range_oid=3910, subtype_oid=1184),
        # autogenerated: end
    ]:
        types.add(t)


def register_default_adapters(context: AdaptContext) -> None:
    from .types import array, bool, composite, datetime, enum, json, multirange, net
    from .types import none, numeric, numpy, range, string, uuid

    array.register_default_adapters(context)
    composite.register_default_adapters(context)
    datetime.register_default_adapters(context)
    enum.register_default_adapters(context)
    json.register_default_adapters(context)
    multirange.register_default_adapters(context)
    net.register_default_adapters(context)
    none.register_default_adapters(context)
    range.register_default_adapters(context)
    string.register_default_adapters(context)
    uuid.register_default_adapters(context)

    # Both numpy Decimal and uint64 dumpers use the numeric oid, but the former
    # covers the entire numeric domain, whereas the latter only deals with
    # integers. For this reason, if we specify dumpers by oid, we want to make
    # sure to get the Decimal dumper. We enforce that by registering the
    # numeric dumpers last.
    numpy.register_default_adapters(context)
    bool.register_default_adapters(context)
    numeric.register_default_adapters(context)
