#!/usr/bin/env pytest
# SPDX-License-Identifier: WTFPL

from pathlib import Path
import subprocess

import pytest


@pytest.mark.parametrize(
	"input,output",
	[
		("sos", "... --- ..."),
		("SoS", "... --- ..."),
		("hello world", ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."),
	]
)
def test_text_to_morse(input, output):
	got = subprocess.check_output(
		["./morse"],
		encoding="utf-8",
		input=input,
		cwd=Path(__file__).parent,
	).rstrip()
	assert got == output


@pytest.mark.parametrize(
	"input,output",
	[
		("... --- ...", "SOS"),
		(".... . .-.. .-.. --- / .-- --- .-. .-.. -..", "HELLO WORLD"),
	]
)
def test_morse_to_text(input, output):
	got = subprocess.check_output(
		["./morse", "--parse"],
		encoding="utf-8",
		input=input,
		cwd=Path(__file__).parent,
	).rstrip()
	assert got == output
