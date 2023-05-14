#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import enum
import re

import PyQt6.QtCore
import PyQt6.QtGui
import PyQt6.QtWidgets


REPLACEMENTS = {}


def process_obj(obj):
    try:
        obj_name = obj.__name__
    except AttributeError:
        return

    REPLACEMENTS[obj_name] = {
        entry.name: f"{enum_name}.{entry.name}"
        for enum_name in dir(obj)
        if enum_name[0].isupper()
        for sub_obj in (getattr(obj, enum_name),)  # XXX hack to emulate walrus
        if isinstance(sub_obj, type) and issubclass(sub_obj, enum.Enum)
        for entry in sub_obj
    }


def process_module(module):
    for attr in dir(module):
        obj = getattr(module, attr)
        process_obj(obj)


def main():
    parser = argparse.ArgumentParser(
        description="Dumb port FILE from PyQt5 to PyQt6, such as enums, exec_, etc."
    )
    parser.add_argument("-d", action="store_true")
    parser.add_argument("file")
    args = parser.parse_args()

    process_module(PyQt6.QtCore)
    process_module(PyQt6.QtGui)
    process_module(PyQt6.QtWidgets)

    if args.d:
        import json; print(json.dumps(REPLACEMENTS, indent=2))

    with open(args.file) as fp:
        text = fp.read()

    new_replace = {}
    for obj_name, obj_replaces in REPLACEMENTS.items():
        for old, new in obj_replaces.items():
            new_replace[f"{obj_name}.{old}"] = f"{obj_name}.{new}"

    def do_replace(match):
        return new_replace[match[0]]

    bigsearch = "|".join(re.escape(pattern) for pattern in new_replace)
    text = re.sub(fr"\b(?:{bigsearch})\b", do_replace, text)

    text = re.sub(r"\bPyQt5\b", "PyQt6", text)
    text = re.sub(r"\bexec_\(", "exec(", text)

    m = re.search("mouse(?:Press|Move|Release)Event", text)
    if m:
        print(f"warning: {m[0]} is used, QMouseEvent interface changed")
    m = re.search("QAction|QFileSystemModel", text)
    if m:
        print(f"warning: {m[0]} moved to PyQt6.QtGui")
    if "qApp" in text:
        print("warning: qApp has been removed")

    with open(args.file, "w") as fp:
        fp.write(text)


if __name__ == "__main__":
    main()
