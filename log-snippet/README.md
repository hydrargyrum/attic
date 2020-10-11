# log-snippet

log-snippet takes an arbitrary "compilation-log" and shows contextual lines, a bit like `grep -C`

# Synopsis

	log-snippet [-C CONTEXTLINES] < LOG

# Example

Take for example the output of `flake8` command:

```
% flake8 bad.py other.py 
bad.py:4:8: E225 missing whitespace around operator
bad.py:17:5: E303 too many blank lines (2)
other.py:3:10: E201 whitespace after '('
```

... which yields filenames and line numbers, one per line.

For each file/line number, `log-snippet` will show the content of the line number of the file, with optional context lines.

For example, pipe `flake8` output into `log-snippet` and show up to 2 lines before and 2 lines after around the mentioned line:

```
% flake8 bad.py other.py | ~/progextern/attic/log-snippet/log-snippet.sh -C 2
bad.py-2-
bad.py-3-def foo1():
bad.py:4:    qux=1
bad.py-5-    print(qux)
bad.py-6-
--
bad.py-15-
bad.py-16-
bad.py:17:    c = 3
bad.py-18-    print(a, b, c)
--
other.py-1-
other.py-2-
other.py:3:def foo2( ):
other.py-4-    if(1):
other.py-5-        print('foo')
```

The default is `-C 5`.

# Compilation log format

The format accepted by log-snippet is used by many compilers and linters, for example flake8, gcc, etc.

`log-snippet` output format is similar to the format returned by `grep -H -n -C 5`.
