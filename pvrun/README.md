# pvrun

Run a command and show its I/O progress with pv(1).

# Synopsis

	pvrun COMMAND [ARGUMENTS...]

# Description

Run COMMAND ARGUMENTS and show its I/O progress with pv(1).
pv can follow file descriptors of a command and display
progress bars.

# Example

The simple command

	cp bigfile.tar /destination

copies a file, but it displays no progress information about the data
processed so far, its speed or ETA. Instead, we can simply wrap it with `pvrun`

	pvrun cp bigfile.tar /destination

which runs the regular cp command, but also displays progress bars.

`pvrun` can do the same with other commands:

	pvrun tar cfz destination.tar.gz /dir/full/of/files

# Requirements

The `pv` command must be installed, as it does the heavy lifting of tracking
file descriptors, showing progress bars, etc.

# License

This is free software, distributed under the WTFPL 2.0.
