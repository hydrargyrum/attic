#!/usr/bin/env pytest
# SPDX-License-Identifier: WTFPL

import json
import os
import subprocess

import pytest


os.chdir(os.path.dirname(__file__))


def run(input):
	return json.loads(subprocess.check_output(
		["./pyliteral-to-json"],
		encoding="utf8",
		input=input
	))


def test_basic():
	assert run("""{0o1: u'2', 0x3: None,}""") == {"1": "2", "3": None}


def test_error():
	with pytest.raises(subprocess.CalledProcessError):
		run("[1+1]")

	with pytest.raises(subprocess.CalledProcessError):
		run("[id(1)]")

	with pytest.raises(subprocess.CalledProcessError):
		run("[datetime(1+1)]")


def test_datetime():
	assert run("""[datetime(2013, 4, 5)]""") == ["2013-04-05 00:00:00"]


def test_decimal():
	assert run("""[Decimal('1')]""") == ["1"]


def test_set():
	assert run("""set()""") == []
	assert run("""frozenset()""") == []
	assert run("""frozenset({1})""") == [1]
