#!/usr/bin/env python3

import pathlib
import subprocess


output = subprocess.check_output(
	[pathlib.Path(__file__).with_name('ts-diff.py')],
	encoding='utf-8',
	input='''
2020-11-09 19:24:08,582:FOO
EXTRA
2020-11-09 19:24:08,628:BAR
2020-11-09 19:24:08,351:BAZ
LINE
	'''.strip()
)
assert output == '''
2020-11-09 19:24:08,582:FOO
EXTRA
+0.046s :BAR
-0.277s :BAZ
LINE
'''.lstrip()
