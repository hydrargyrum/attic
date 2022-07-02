# boxuni

Given this table (which can be generated with `csv2table.py --header sample.csv`):

```
+----------+--------+
| name     | color  |
+----------+--------+
| zucchini | green  |
| tomato   | red    |
| banana   | yellow |
| orange   | orange |
+----------+--------+
```

When passing it to stdin of `boxuni`, it is converted to prettier, Unicode-based:

```
┌──────────┬────────┐
│ name     │ color  │
├──────────┼────────┤
│ zucchini │ green  │
│ tomato   │ red    │
│ banana   │ yellow │
│ orange   │ orange │
└──────────┴────────┘
```
