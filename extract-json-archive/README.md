# extract-json-archive

## Usage

```
extract-json-archive [-o DIRECTORY] INPUT.ARCHIVE.JSON
```

## Format

```json
[
    {
        "filename": "hello.txt",
        "data": "SGVsbG8gd29ybGQhCg=="
    },
    {
        "filename": "black-pixel.gif",
        "data": "R0lGODlhAQABAPAAAAAAAAAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw=="
    },
    ...
]
```

- absolute paths (e.g. `"/foo/bar"`) are not allowed
- relative paths pointing to parent directories (e.g. `"../foo/bar"`) are not allowed
- directories should be implicitly created (e.g. `"foo/bar/baz"` should create `foo` and `foo/bar` directories)
- `data` is in base64 (non-URL-safe) format
