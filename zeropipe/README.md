# zeropipe

zeropipe is a wrapper for other programs that have the ability to take NULL-separated "lines" instead of newline-separated lines.
It's merely a shorthand for not having to remember the correct option name.

For example, `xargs` uses `-0`, but `grep` uses `-z`. `zeropipe` is here to remember it for you.

Here's a command for removing those useless `__MACOSX` folders some non-free OS insists on polluting you with:

    locate -0 __MACOSX | grep -z 'OSX$' | xargs -0 rm -vr

The same command with zeropipe:

    zeropipe locate __MACOSX | zeropipe grep 'OSX$' | zeropipe xargs rm -vr

## Supported commands

zeropipe accepts:

- find
- fzf
- grep
- head
- locate
- ls
- sed
- sort
- tail
- uniq
- xargs
