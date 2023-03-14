# json-elide-strings

Elide too long strings in JSON data

## Usage

```
json-elide-strings [--length=N] [--keys] [--suffix=ELLIPSIS] [FILE]
```

## Sample

```
% cat long.json
{
  "foo": [
    "barrrrrrrrrrrrrrrrrr",
    {
      "baz": "quuuuuuuuuuuuuuux"
    }
  ]
}
% json-elide-strings --length=6 < long.json
{
  "foo": [
    "bar...",
    {
      "baz": "quu..."
    }
  ]
}
```
