# flatten-json

Flatten a deep JSON structure in a flat object with path-like keys

# Synopsis

	flatten-json [--expand [--no-lists]] [--separator CHAR]

# Example

Given the following JSON:

```json
{
    "my_object": [
        {
            "id": "foo",
            "name": "Foo!",
            "description": "blah blah"
        },
        {
            "id": "bar",
            "name": "Bar..."
        }
    ],
    "something": "whatever"
}
```

`flatten-json` will output this:

```json
{
  "my_object/0/id": "foo",
  "my_object/0/name": "Foo!",
  "my_object/0/description": "blah blah",
  "my_object/1/id": "bar",
  "my_object/1/name": "Bar...",
  "something": "whatever"
}
```

A flat JSON with only one level of depth and path-like keys.

# Options

	--expand

Do the reverse operation, take a flat JSON with path-like keys and transform in tree JSON

	--no-lists

(Only applicable if `--expand` is given), when faced with numeric elements in path, do not try to build a list/array, build an object with numeric keys.

	--separator CHAR

Use CHAR instead of `/` as path separator. Applicable for both `--expand` and `--flatten`.
