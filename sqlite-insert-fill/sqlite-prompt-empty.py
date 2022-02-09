#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import sqlite3
import random

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


def q(identifier):
    if not identifier.isidentifier():
        raise ValueError(f"Name {identifier!r} contains forbidden chars")
    return '"' + identifier + '"'


def chooser(elements, tagcol, isenum):
    if isenum:
        *alltags, = sorted({
            tags
            for tags in elements.values()
            if tags and isinstance(tags, str)
        })
    else:
        *alltags, = sorted({
            tag
            for tags in elements.values()
            if tags and isinstance(tags, str)
            for tag in tags.split()
        })
    completer = WordCompleter(alltags)
    return prompt(f'tags({tagcol}): ', completer=completer)


parser = argparse.ArgumentParser()
parser.add_argument("--id-column", default="rowid")
parser.add_argument("--name-column", default="name")
parser.add_argument("--enum", action="store_true")
parser.add_argument("database")
parser.add_argument("table")
parser.add_argument("column")
args = parser.parse_args()

db = sqlite3.connect(args.database)
fillcol = args.column
with db:
    elements = {
        (row[0], row[1]): row[2]
        for row in
        db.execute(f"""
            select {q(args.id_column)}, {q(args.name_column)}, {q(fillcol)}
            from {q(args.table)}
        """)
    }
    tofill = {
        idname
        for idname, value in elements.items()
        if value in (None, "")
    }
    idname = random.choice(list(tofill))
    print(f"{idname[1]} ({len(tofill)} left)")
    tags = chooser(elements, fillcol, args.enum)
    if tags:
        db.execute(
            f"""
                update {q(args.table)}
                set {q(fillcol)} = ?
                where {q(args.id_column)} = ?
            """,
            (tags, idname[0])
        )
