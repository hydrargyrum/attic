#!/usr/bin/env python3

import argparse
import ast
import locale
import os
import re
import sys


op_to_str = {
    ast.And: "and",
    ast.Or: "or",

    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Pow: "**",
    ast.MatMult: "@",
    ast.Div: "/",
    ast.FloorDiv: "//",
    ast.Mod: "%",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitOr: "|",
    ast.BitXor: "^",
    ast.BitAnd: "&",

    ast.UAdd: "+",
    ast.USub: "-",
    ast.Not: "not",
    ast.Invert: "~",

    ast.Is: "is",
    ast.IsNot: "is not",
    ast.In: "in",
    ast.NotIn: "not in",
    ast.Eq: "==",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">=",
    ast.NotEq: "!=",
}


def has_colors(fp=sys.stdout):
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("CLICOLOR_FORCE") or os.environ.get("FORCE_COLOR"):
        return True
    return fp.isatty()


def unparse(node):
    match node:
        case ast.BoolOp():
            return "(" + f" {op_to_str[type(node.op)]} ".join(unparse(sub) for sub in node.values) + ")"
        case ast.BinOp():
            return f"({unparse(node.left)} {op_to_str[type(node.op)]} {unparse(node.right)})"
        case ast.UnaryOp():
            return f"({unparse(type(node.op))} {unparse(node.operand)})"
        case ast.Compare():
            return f"({unparse(node.left)} " + " ".join(f"{op_to_str[type(op)]} {unparse(val)}" for op, val in zip(node.ops, node.comparators)) + ")"
        case ast.Attribute():
            return f"{unparse(node.value)}.{node.attr}"
            #return f"({unparse(node.value, no_par=True)}.{node.attr})"
        case ast.Constant() | ast.Name():
            return ast.unparse(node)
        case ast.IfExp():
            return f"({unparse(node.body)} if {unparse(node.test)} else {unparse(node.orelse)})"

    raise NotImplementedError(type(node).__name__)


try:
    import colorama
except ImportError:
    def color_par(line):
        return line
else:
    def color_par(line):
        if not has_colors():
            return line
        COLORS = [
            colorama.Fore.LIGHTRED_EX, colorama.Fore.LIGHTGREEN_EX,
            colorama.Fore.LIGHTBLUE_EX, colorama.Fore.LIGHTCYAN_EX,
            colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.LIGHTYELLOW_EX,
        ]

        result = ""
        level = -1
        while True:
            m = re.search("[()]", line)
            if not m:
                return result + line
            if m[0] == "(":
                level += 1
            result += line[:m.start()] + COLORS[level] + m[0] + colorama.Fore.RESET
            line = line[m.end():]
            if m[0] == ")":
                level -= 1


def main():
    locale.setlocale(locale.LC_ALL, "")

    parser = argparse.ArgumentParser()
    parser.add_argument("expr", help="expression on which to make priorities explicit")
    args = parser.parse_args()

    root = ast.parse(args.expr, mode="eval")
    result = unparse(root.body).removeprefix("(").removesuffix(")")
    result = color_par(result)
    print(result)


if __name__ == "__main__":
    main()
