#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import re

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QClipboard
from PyQt6.QtWidgets import (
    QSizePolicy, QStyle, QRubberBand, QDialogButtonBox, QDialog, QMessageBox,
)


REPLACEMENTS = {}


def process_obj(obj):
    REPLACEMENTS[obj.__name__] = {
        entry.name: f"{enum_name}.{entry.name}"
        for enum_name in dir(obj)
        if enum_name[0].isupper()
        for entry in getattr(obj, enum_name)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Dumb port FILE from PyQt5 to PyQt6, such as enums, exec_, etc."
    )
    parser.add_argument("file")
    args = parser.parse_args()

    process_obj(Qt)
    process_obj(QKeySequence)
    process_obj(QClipboard)
    process_obj(QSizePolicy)
    process_obj(QStyle)
    process_obj(QRubberBand)
    process_obj(QDialog)
    process_obj(QDialogButtonBox)
    process_obj(QMessageBox)

    with open(args.file) as fp:
        text = fp.read()

    for obj_name, obj_replaces in REPLACEMENTS.items():
        for old, new in obj_replaces.items():
            text = re.sub(fr"\b{obj_name}\.{old}\b", fr"{obj_name}.{new}", text)

    text = re.sub(r"\bPyQt5\b", "PyQt6", text)
    text = re.sub(r"\bexec_\(", "exec(", text)

    m = re.search("mouse(?:Press|Move|Release)Event", text)
    if m:
        print(f"warning: {m[0]} is used, QMouseEvent interface changed")
    if "QAction" in text:
        print("warning: QAction moved to PyQt6.QtGui")
    if "qApp" in text:
        print("warning: qApp has been removed")

    with open(args.file, "w") as fp:
        fp.write(text)


if __name__ == "__main__":
    main()
