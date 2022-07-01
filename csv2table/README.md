# csv2table

Given this `sample.csv`:

```
name,color
zucchini,green
tomato,red
banana,yellow
orange,orange
```

When running `csv2table.py --header sample.csv`, the following table is output:

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
