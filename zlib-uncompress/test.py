#!/usr/bin/env pytest

import os
import subprocess
import sys


os.chdir(os.path.dirname(__file__))


def test_basic():
    out = subprocess.check_output(
        [sys.executable, "./zlib-uncompress"],
        input=b"x\x9c\xf3H\xcd\xc9\xc9W(\xcf/\xcaIQ\x04\x00\x1d\t\x04^",
    )
    assert out == b"Hello world!"
