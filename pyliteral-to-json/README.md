# pyliteral-to-json

Convert python literal dict/list/string to JSON.

## description

Some python programs log data without formatting it in JSON so it may look like this, mostly because python's string representation favours single quotes:

```
{'foo': 'bar', 'baz': True}
```

It looks similar to JSON, but it's not, only python can handle that.
`pyliteral-to-json` reads from stdin and transforms it into:

```json
{"foo": "bar", "baz": true}
```

which can be given to any tool supporting JSON. It can then be [processed](https://gitlab.com/hydrargyrum/pjy), [flattened](https://gitlab.com/hydrargyrum/attic/-/tree/master/flatten-json), [folded](https://gitlab.com/hydrargyrum/foldindent)… you name it.

The goal is not to parse python code, only to parse something that's output when doing `print(my_object)`, for common types.

## handled types

`pyliteral-to-json` interprets types that map natively to JSON:

- `None`/booleans/ints/floats/strings literals
- list/dicts

but it can also map:

- tuples and sets like `{1, 2, 3}` or `set()` and convert them to JSON arrays
- naive datetime objects like `datetime.datetime(2023, 3, 10, 15, 26, 12, 273109)` and convert them to JSON strings
- `UUID('00000000-0000-0000-0000-000000000000')` syntax and convert to JSON strings
- `PosixPath('/foo')` and convert to JSON string

## security and "no eval"

`pyliteral-to-json` does not use the infamous `eval()` but `ast.literal_eval()` and thus is somewhat safe, as it will not try to run or import untrusted code.
However, [its documentation mentions](https://docs.python.org/3/library/ast.html#ast.literal_eval):

> A relatively small input can lead to memory exhaustion or to C stack exhaustion, crashing the process. There is also the possibility for excessive CPU consumption denial of service on some inputs. Calling it on untrusted data is thus not recommended.

So, keep that in mind when using it.
