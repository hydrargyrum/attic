#!/usr/bin/env python3
# license: Do What The Fuck You Want To Public License version 2 [http://www.wtfpl.net/]

import pathlib
import subprocess


output = subprocess.check_output(
	[pathlib.Path(__file__).with_name('log-ts-diff.py')],
	encoding='utf-8',
	input='''
2020-11-09 19:24:08,582:FOO
EXTRA
2020-11-09 19:24:08,628:BAR
2020-11-09 19:24:08,351:BAZ
2020-11-09 19:24:09,351:QUX
LINE
	'''.strip()
)
assert output == '''
2020-11-09 19:24:08,582:FOO
EXTRA
+ 0.046s :BAR
- 0.277s :BAZ
+ 1s :QUX
LINE
'''.lstrip()
