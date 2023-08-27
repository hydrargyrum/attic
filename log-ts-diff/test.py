#!/usr/bin/env pytest
# SPDX-License-Identifier: WTFPL

from textwrap import dedent
import pathlib
import subprocess


cmd = pathlib.Path(__file__).with_name('log-ts-diff.py')


def test_basic():
	output = subprocess.check_output(
		[cmd],
		encoding='utf-8',
		input=dedent("""
			2020-11-09 19:24:08,582:FOO
			EXTRA
			2020-11-09 19:24:08,628:BAR
			2020-11-09 19:24:08,351:BAZ
			2020-11-09 19:24:09,351:QUX
			LINE
		""").strip()
	)
	assert output == dedent("""
		2020-11-09 19:24:08,582:FOO
		EXTRA
		+ 0.046s :BAR
		- 0.277s :BAZ
		+ 1s :QUX
		LINE
	""").lstrip()
