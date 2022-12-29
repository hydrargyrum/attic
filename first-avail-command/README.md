# first-avail-command

`first-avail-command` is a command wrapper designed to be put in configuration files:

- where a command is accepted
- and there are several alternatives for the same task
- but it's not known which alternative is installed

## Synopsis

```
first-avail-command ALTERNATIVE1 ALTERNATIVE2 [...] -- ARGS FOR COMMAND
```

In a config file, it should typically be called like this:

```
first-avail-command ALTERNATIVE1 ALTERNATIVE2 ALTERNATIVE3 --
```

The external runner will pass its own args after the `--`.
`first-avail-command` will choose the first installed alternative and feed it the external args passed after `--`.

## Samples

### `~/.gitconfig`

```
[pager]
    diff = first-avail-command delta batcat bat diff-so-fancy --
```

#### What are those commands?

- [delta](https://github.com/dandavison/delta)
- [bat](https://github.com/sharkdp/bat) (or `batcat` on some systems)
- [diff-so-fancy](https://github.com/so-fancy/diff-so-fancy)

### Shell config: fzf

```
export FZF_DEFAULT_COMMAND="first-avail-command fd 'rg --files' find --"
```

This sample shows in addition how to pass some arguments that are specific to an alternative: here, `rg` must be passed `--files`, but not other alternatives.

#### What are those commands?

- [fzf](https://github.com/junegunn/fzf)
- [rg](https://github.com/BurntSushi/ripgrep)
- [fd](https://github.com/sharkdp/fd)

### Shell config: ls

```
alias ll="first-avail-command exa ls -- -l"
```

This sample shows in addition how to feed some extra arguments in config, which must be allowed by all alternatives: here, both `ls` and `exa` will receive `-l`, in addition of args passed to the `ll` alias.

#### What are those commands?

- [exa](https://the.exa.website/)
