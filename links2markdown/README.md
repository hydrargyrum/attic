# links2markdown

## Usage

```
links2markdown [FILE]
```

## Description

If a text file contains:

```
foo
bar https://example.com baz
qux
```

`links2markdown` will fetch the pages linked and insert the titles this way:

```
foo
bar [title of the page linked](https://example.com) baz
qux
```

