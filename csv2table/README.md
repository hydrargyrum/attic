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

## Options

### CSV format

- `--delimiter=X`: use CSV delimiter instead of comma

### Output

- `--header`: CSV input contains a header line (and so will the output)
- `--box`: use Unicode box characters instead of plain ASCII
- `--markdown`: show table in markdown format
