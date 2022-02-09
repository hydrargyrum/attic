#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

from pathlib import Path
import subprocess


tests = """
| foo | bar |
| long text | other                                                |
| x | y |

+---+--+
| foo | bar |
+-------+--+
| a | b |
+-------+--+
| c | d |
+-------+--+

┌─────┬─────┐
│ foo │ bar │
├─────┼─────┤
│  a  │  b  │
│  c  │  d  │
└─────┴─────┘

--------
| 1 | 2 | 3 |
-----------------------
| 4 | 5 | 6 |
========
| 7 | 8 | nine |
""".strip().split('\n\n')


expecteds = """
+-----------+-------+
|    foo    |  bar  |
+-----------+-------+
| long text | other |
|     x     |   y   |
+-----------+-------+

+-----+-----+
| foo | bar |
+-----+-----+
|  a  |  b  |
|  c  |  d  |
+-----+-----+

+-----+-----+
| foo | bar |
+-----+-----+
|  a  |  b  |
|  c  |  d  |
+-----+-----+

+---+---+------+
| 1 | 2 |  3   |
+---+---+------+
| 4 | 5 |  6   |
| 7 | 8 | nine |
+---+---+------+
""".strip().split('\n\n')


def run_one(test, expected):
    output = subprocess.check_output(
        [Path(__file__).resolve().with_name('realign-text-table')],
        input=test, encoding='utf-8'
    ).rstrip('\n')
    expected = expected.rstrip('\n')
    assert output == expected


def test_basic():
    assert len(tests) == len(expecteds)
    for test, expected in zip(tests, expecteds):
        run_one(test, expected)
        run_one(expected, expected)


doc_test = """
a document

    something

this is a table:

| foo | bar |
| long text | other                                                |
| x | y |

end
"""

doc_expected = """
a document

    something

this is a table:

+-----------+-------+
|    foo    |  bar  |
+-----------+-------+
| long text | other |
|     x     |   y   |
+-----------+-------+

end
"""


def test_embedded():
    run_one(doc_test, doc_expected)
