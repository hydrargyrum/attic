# with-same-shebang: run a command with the same interpreter as another command

Run COMMAND ARGS… through the same interpreter as specified in REF_COMMAND's shebang.
For example if `foo` has this shebang: `#!/bin/bar -f`, then running:

    with-same-shebang foo qux

will run in the end:

    /bin/bar -f qux


## use case: run something in the same python virtual env as a command

Commands that were installed inside a virtual env typically contain the location of the associated virtual env in the shebang.
By using the right interpreter, the whole venv will be activated.
This is especially useful with pipx where the venv location of an installed command may be private otherwise.

```
% pipx install foobar
% python
>>> import foobar
error
% with-same-shebang foobar
>>> import foobar
>>>
```

## Dependencies

with-same-shebang requires a POSIX shell and `sed`, nothing exotic
