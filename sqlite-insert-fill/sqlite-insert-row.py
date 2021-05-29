#!/usr/bin/env python3
# license: WTFPLv2 [http://www.wtfpl.net/]

# yes this program contains a lot of injected strings in SQL requests
# but identifiers aren't parametrizable, plus they are quoted in a strict way

from argparse import ArgumentParser
from sqlite3 import connect, Row

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import PromptSession


def q(identifier: str):
    if not identifier.isidentifier():
        raise ValueError(f"Name {identifier!r} contains forbidden chars")
    # naive quoting, yes but we only accept only a strict subset of chars
    return '"' + identifier + '"'


def insert(obj: dict):
    db.execute(
        f"insert into {q(args.table)} "
        + f"({','.join(q(name) for name in obj)}) "
        + f"values({','.join('?' for _ in obj)}) ",
        tuple(obj.values())
    )


def get_completions(col: str) -> set:
    return {
        word
        for row in db.execute(f"select {q(col)} from {q(args.table)}")
        if row[0]
        for word in row[0].split()
    }


def coerce_to_sql(val: str, sql_type: str):
    if sql_type == "text":
        return val
    elif sql_type == "integer":
        return int(val)
    elif sql_type == "real":
        return float(val)
    else:
        raise AssertionError(f"unhandled {sql_type} type")


def confirm_keep(obj: dict) -> bool:
    rows = db.execute(
        f"""
                select * from {q(args.table)}
                where {' and '.join(f'{q(name)} = ?' for name in args.search_existing)}
        """,
        tuple(obj[col] for col in args.search_existing)
    )
    has_rows = False
    for row in rows:
        has_rows = True
        print(f"found similar object:")
        for col in dict(row):
            print(f"  {col}: {row[col]}")
        print()

    if has_rows:
        return confirm("continue? ")
    return True


def prompt_obj():
    obj = {}
    done_existing = False

    for col, col_type in col_types.items():
        if col in default_set:
            obj[col] = default_set[col]
            continue

        elif col_type == "text":
            val = session.prompt(
                f"{col}? ",
                completer=WordCompleter(get_completions(col)),
                complete_while_typing=True,
            )
            if not val:
                val = None
            obj[col] = val

        elif col_type in ("integer", "real"):
            val = session.prompt(f"{col}? ")
            if val:
                val = coerce_to_sql(val, col_type)
            else:
                val = None
            obj[col] = val

        if (
            args.search_existing
            and not done_existing
            # search only when required fields are filled
            and set(obj) >= set(args.search_existing)
        ):
            done_existing = True
            if not confirm_keep(obj):
                return None

    return obj


def confirm(msg: str = 'confirm? ') -> bool:
    while True:
        rep = session.prompt(msg, completer=WordCompleter([]))
        if rep in ('y', 'n'):
            break
    return {'y': True, 'n': False}[rep]


# args
parser = ArgumentParser()
parser.add_argument("database")
parser.add_argument("table")
parser.add_argument("--set", action="append")
parser.add_argument("--search-existing")
args = parser.parse_args()

# parsing
default_set = dict(
    tuple(arg.split("=", 1))
    for arg in (args.set or ())
)

if args.search_existing:
    args.search_existing = args.search_existing.split(",")

# db
db = connect(args.database)
db.row_factory = Row

col_types = {
    row["name"]: row["type"].lower()
    for row in db.execute(f"pragma table_info({q(args.table)})")
}

# main
session = PromptSession()

obj = prompt_obj()

if obj:
    print(f"about to insert:")
    max_name = max(len(col) for col in obj)
    for col in obj:
        print(f"  {col:{max_name}}: {obj[col]}")
    print()

    if confirm():
        with db:
            insert(obj)
