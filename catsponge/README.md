# why catsponge?

So-called "filter" command-line programs read input on stdin and print it slightly modified on stdout, like sed or grep.
When pasting long text to the terminal to a filter program, the output can easily be mixed with the input on the terminal, which is very confusing.

One way to circumvent it is to add this after the filter arguments: `> tmpfile ; cat tmpfile ; rm tmpfile`.
And that's exactly what catsponge does (with a proper temp file).

Pipe catsponge before the filter program, and the filter will be able to read its input only when stdin has reached EOF.
Pipe catsponge after the filter program, and the output of the filter will be shown only when the output is complete (because stdin has reached EOF).
In this way, the filter's output comes only after the whole input.
