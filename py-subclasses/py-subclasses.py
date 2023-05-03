#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import importlib
import sys


def print_subtree(cls, indent=""):
    print(f"{indent}{cls}")
    for sub in cls.__subclasses__():
        print_subtree(sub, indent + "    ")


def main():
    parser = argparse.ArgumentParser(
        description="Show found subclasses of a class.",
        epilog="Subclasses are only found if their module is imported, make sure"
        + " to pass arguments to import modules that may contain them.",
    )
    parser.add_argument(
        "modules", nargs="*",
        help="Modules to import, that may contain subclasses",
    )
    parser.add_argument(
        "class_name",
        help="Full path of the class of which to print subclasses"
        + " (e.g. collections.abc.Sequence)",
    )
    args = parser.parse_args()

    module_names = args.modules
    module, _, symbol = args.class_name.rpartition(".")
    module_names.append(module)

    for name in module_names:
        importlib.import_module(name)

    cls = getattr(sys.modules[module], symbol)
    print_subtree(cls)


if __name__ == "__main__":
    main()
