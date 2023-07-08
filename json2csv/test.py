#!/usr/bin/env pytest

import os
import subprocess

import pytest


os.chdir(os.path.dirname(__file__))


def run(args, input):
    return subprocess.check_output(
        ["./json2csv", *args],
        input=input, encoding="utf8"
    )


def dedent(text):
    # text is indented in our tests but the expected output isn't
    return "\n".join(line.strip() for line in text.split("\n"))


@pytest.mark.parametrize(
    "args,input,output",
    [
        # basic dict of arrays
        (
            (),
            """{"foo": [1, 2, 3], "bar": [4, 5, 6]}""",
            """
            foo,bar
            1,4
            2,5
            3,6
            """,
        ),
        # custom separator
        (
            ("-s", ";"),
            """{"foo": [1, 2, 3], "bar": [4, 5, 6]}""",
            """
            foo;bar
            1;4
            2;5
            3;6
            """,
        ),
        # filter by chosen keys
        (
            ("-k", "bar"),
            """{"foo": [1, 2, 3], "bar": [4, 5, 6]}""",
            """
            bar
            4
            5
            6
            """,
        ),
        # filter multiple keys
        (
            ("-k", "foo", "bar"),
            """{"foo": [1, 2, 3], "bar": [4, 5, 6]}""",
            """
            foo,bar
            1,4
            2,5
            3,6
            """,
        ),
        # chosen keys as first
        (
            ("bar",),
            """{"foo": [1, 2, 3], "bar": [4, 5, 6]}""",
            """
            bar,foo
            4,1
            5,2
            6,3
            """,
        ),
        # basic array of dicts
        (
            (),
            """[{"foo": 1, "bar": 4},{"foo": 2, "bar": 5}, {"bar": 6, "foo": 3}]""",
            """
            foo,bar
            1,4
            2,5
            3,6
            """,
        ),
        # escape data
        (
            (),
            r"""{"foo": ["c,o,m,m,a", "s p a c e s are"], "bar": ["text with \"quotes\"", "ok"]}""",
            '''
            foo,bar
            "c,o,m,m,a","text with ""quotes"""
            s p a c e s are,ok
            ''',
        ),
        # basic json lines
        (
            (),
            """["foo","bar"]\n[1,2]\n[3,4]\n""",
            """
            foo,bar
            1,2
            3,4
            """
        ),
        (
            (),
            """{"foo":1,"bar":2}\n{"bar":4,"foo":3}\n""",
            """
            foo,bar
            1,2
            3,4
            """
        ),
    ]
)
def test_simple(args, input, output):
    # the process adds a final newline
    assert run(args, input.strip()) == dedent(output.strip()) + "\n"


# TODO test separate file
# TODO test errors
# TODO test inconsistent array length
# TODO test missing keys
