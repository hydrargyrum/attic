# pyliteral-to-json

Convert python literal dict/list/string to JSON.

Some python programs log data without formatting it in JSON so it may look like this, mostly because python's string representation favours single quotes:

```
{'foo': 'bar', 'baz': True}
```

With longer and deeper-nested objects, this is cumbersome to work with because only python can handle that.
`pyliteral-to-json` transforms it into:

```json
{"foo": "bar", "baz": true}
```

which can be given to any tool supporting JSON. It can then be [processed](https://gitlab.com/hydrargyrum/pjy), [flattened](https://gitlab.com/hydrargyrum/attic/-/tree/master/flatten-json), [folded](https://gitlab.com/hydrargyrum/foldindent)… you name it.

## no eval

`pyliteral-to-json` does not use the infamous `eval()`.

## datetimes

`pyliteral-to-json` also interprets naive datetime objects like `datetime.datetime(2023, 3, 10, 15, 26, 12, 273109)` and convert them to JSON strings.
