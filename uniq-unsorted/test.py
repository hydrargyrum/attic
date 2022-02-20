#!/usr/bin/env pytest
# SPDX-License-Identifier: WTFPL

import os
from pathlib import Path
import signal
import subprocess
import time

import pytest


app_exe = str(Path(__file__).with_name("uniq-unsorted.py"))


@pytest.mark.parametrize(
	"input,expected",
	[
		(["foo", "bar"], ["foo", "bar"]),
		(["foo", "foo", "bar"], ["foo", "bar"]),
		(["foo", "bar", "bar"], ["foo", "bar"]),
		(["foo", "bar", "foo"], ["foo", "bar"]),
		(["foo", "bar", "foo", "bar"], ["foo", "bar"]),
		(["foo", "bar", "foo", "qux", "bar"], ["foo", "bar", "qux"]),
	]
)
def test_basic(input, expected):
	input = "\n".join(input + [""])
	expected = "\n".join(expected + [""])
	got = subprocess.check_output([app_exe], encoding="utf-8", input=input)
	assert got == expected


@pytest.mark.parametrize(
	"input,expected,encoding",
	[
		(["àccented", "lïñes"], ["àccented", "lïñes"], "utf-8"),
		(["àccented", "lïñes"], ["àccented", "lïñes"], "latin-1"),
		([
			"àccented", "lïñes", "lïñes"], ["àccented", "lïñes"],
			"latin-1"
		),
		(
			["\U0001F44D", "\U0001F44E", "\U0001F44D", "\U0001F44E"],
			["\U0001F44D", "\U0001F44E"], "utf-8"
		),
	]
)
def test_encodings(input, expected, encoding):
	utf8env = {
		**os.environ,
		"PYTHONUTF8": "1",
		"PYTHONIOENCODING": "utf-8",
	}

	input = "\n".join(input + [""]).encode(encoding)
	expected = "\n".join(expected + [""])
	got = subprocess.check_output([app_exe], input=input, env=utf8env)
	got = got.decode(encoding)
	assert got == expected


@pytest.mark.parametrize("encoding", ("utf-8", "latin-1"))
def test_file(tmp_path, encoding):
	expected = "àccented\nlïñes\n"
	input = "àccented\nlïñes\nàccented\nlïñes\n"

	tmp_file = tmp_path.joinpath("in.txt")
	tmp_file.write_bytes(input.encode(encoding))
	got = subprocess.check_output([app_exe, str(tmp_file)])
	got = got.decode(encoding)

	assert got == expected


def test_interrupt():
	proc = subprocess.Popen([app_exe], stdin=subprocess.PIPE)
	time.sleep(1)
	proc.send_signal(signal.SIGINT)
	assert proc.wait(1) == -2


def test_broken_pipe():
	p1 = subprocess.Popen(
		[app_exe], stdout=subprocess.PIPE,
		stdin=subprocess.PIPE, encoding="utf-8",
	)
	p2 = subprocess.Popen(
		["head", "-1"], stdin=p1.stdout, stdout=subprocess.PIPE,
	)
	p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
	p1.stdin.write("\n".join(str(i) for i in range(10000)))
	p1.stdin.close()
	output = p2.communicate()[0]

	assert output == b"0\n"
	assert p2.returncode == 0
	assert p1.wait(1) == 0
