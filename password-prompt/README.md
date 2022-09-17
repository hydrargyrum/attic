# password-prompt

Glue tool to read a password on tty (not stdin) and print to stdout.

## Synopsis

    passwordprompt [PROMPT STRING]

## Use cases

In shell scripts, add `password=$(prompt-password)` to prompt a password with messing with [`stty(1)`](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/stty.html).

Some apps read passwords from env variables, files or customizable commands (e.g. to run [`pass`](https://www.passwordstore.org/)), but are incapable of reading passwords interactively themselves.
`prompt-password` is useful here as an external command that will effectively read the password interactively.
Examples:

- [borgmatic](https://torsion.org/borgmatic/) (with `encryption_passcommand: password-prompt`)
- [vdirsyncer](https://vdirsyncer.pimutils.org/en/stable/) (with `password.fetch = ["command", "password-prompt"]`)
- ~~[mbsync](https://isync.sourceforge.io/) (mbsync is able to prompt a password)~~
