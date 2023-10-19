#!/usr/bin/env pytest
# SPDX-License-Identifier: WTFPL

import os
import subprocess

import pytest


os.chdir(os.path.dirname(__file__))


def run(args):
    return subprocess.check_output(
        ["./args2csv", *args],
        encoding="utf8",
    )


@pytest.mark.parametrize(
    "args,output",
    [
        (["foo", "bar baz", "q,u,uu,x"], 'foo,bar baz,"q,u,uu,x"'),
        (["foo", 'bar"baz'], 'foo,"bar""baz"'),
        (["-s", ";", "foo", "bar baz", "q,u,uu,x"], 'foo;bar baz;q,u,uu,x'),
    ]
)
def test_simple(args, output):
    # the process adds a final newline
    assert run(args) == output.strip() + "\n"
