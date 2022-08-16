# The Attic

This repository hosts various small personal tools.

- [`all-clipboard`](all-clipboard): list clipboard data on stdout
- [`altlines`](altlines): mark every 2 lines with color
- [`boxuni`](boxuni): convert ASCII-art boxes into Unicode-art boxes
- [`catsponge`](catsponge): like cat(1) but soaks stdin and waits that stdin reaches EOF
- [`cheapthrottle`](cheapthrottle): throttling a process by sending it SIGSTOP/SIGCONT repeatedly
- [`clipsync`](clipsync):
- [`coordapp`](coordapp): always-on-top window that shows the mouse cursor coordinates
- [`cppasciitree`](cppasciitree): an example of how to hardcode a tree with source code looking like the actual tree
- [`crc`](crc): basic CRC computation tool
- [`csv2json`](csv2json): transform CSV into JSON
- [`csv2table`](csv2table): pretty-print a CSV file with ASCII-art table
- [`exiforientergui`](exiforientergui): GUI to losslessly modify EXIF orientation of an image
- [`ffmcut`](ffmcut): ffmpeg wrapper to cut a video between 2 timestamps
- [`fix-broken-links-by-name`](fix-broken-links-by-name): fix broken symlinks if target file changed dir but not name
- [`flatten-json`](flatten-json): flatten a deep json tree in a single json or reverse operation
- [`fonts2png`](fonts2png): render TTF fonts samples to image files
- [`gen-indexhtml`](gen-indexhtml): create an index.html listing all files in dir
- [`git`](git): misc git utilities
- [`gotify-tools/gotify-push`](gotify-tools/gotify-push.py): command-line tool for pushing a gotify notification
- [`gotify-tools/gotify-read`](gotify-tools/gotify-read.py): command-line tool for listing/reading gotify notifications
- [`group-files-by-mtime`](group-files-by-mtime): take files in a dir and move them to folders for each last modification time
- [`hardlinks-to-csv`](hardlinks-to-csv): list files (and inodes) with more than 1 hardlink as CSV
- [`headset-bluez`](headset-bluez): enable a bluetooth headset and out or in/out mode
- [`hexgen`](hexgen): generate data from an hex dump
- [`hibp`](hibp): check if a password has been leaked on "Have I Been Pwned?" site (by checking hash prefix)
- [`httpshare`](httpshare): share a directory via HTTP, like Python "http.server" but supports "Range" headers
- [`image2xterm`](image2xterm): display an image on console using terminal RGB24 mode or 256 colors
- [`json2csv`](json2csv): transform a JSON list of objects into a CSV file
- [`json2sqlite`](json2sqlite): insert JSON data in SQLite
- [`json2table`](json2table): pretty-print a JSON list of objects in an ASCII-art table
- [`keepassxprint`](keepassxprint): dump info and passwords from a KeePassX database
- [`lch-color-chooser`](lch-color-chooser): CIE LCh color chooser and RGB converter
- [`log-snippet`](log-snippet): parse compilation-log and show snippets of files with context
- [`log-ts-diff`](log-ts-diff): parse log and replace timestamps with diff to previous timestamp
- [`morse`](morse): text from/to Morse code converter, and optional beep player
- [`morsehtml`](morsehtml): HTML page with its background flashing a Morse code message
- [`moversleep`](moversleep): move incoming files from a dir into another
- [`mv-with-thumb`](mv-with-thumb): like mv, but also moves XDG thumbnails
- [`pass-ls-entries`](pass-ls-entries): list pass(1) entries in find(1) format, not tree(1) format
- [`password-prompt`](password-prompt): simply prompt a password on tty and then print it
- [`pdf-watermark`](pdf-watermark): watermark a chosen message on a PDF
- [`pvrun`](pvrun): run a command and show its I/O progress with pv(1)
- [`qgifview`](qgifview): very basic GIF image viewer
- [`qr2unicode`](qr2unicode): display QR-codes on console using Unicode box-drawing characters
- [`qr-shot`](qr-shot): decode a QR code image from part of the screen
- [`qruler`](qruler): tool window that measures width and height in pixels
- [`qunpak`](qunpak): extract Quake I and II .pak files
- [`r2w_plugins`](r2w_plugins): 2 rest2web plugins
- [`radiodump`](radiodump): circular buffer and dump to file
- [`random-line`](random-line): take a random line from stdin
- [`realign-text-table`](realign-text-table): takes a malformed ASCII-drawn table and redraw borders properly
- [`redmine2ical`](redmine2ical): convert Redmine’s timesheet to iCalendar format
- [`screen-msg`](screen-msg): 2 tools for setting screen(1) messages (hardstatus or transient messages)
- [`set-cachedir`](set-cachedir): basic tool to create CACHEDIR.TAG files (prevent a folder from being backed up)
- [`show-args`](show-args): just show args, one per line
- [`sort-with-numbers`](sort-with-numbers): sort stdin like sort(1) but sorts numbers
- [`sqlite-insert-fill`](sqlite-insert-fill): 2 tools for inserting rows and updating others
- [`ssh-tools/ssh-fingerprint-current-host`](ssh-tools/ssh-fingerprint-current-host): show fingerprint of current host ssh server key
- [`ssh-tools/ssh-known-fingerprint`](ssh-tools/ssh-known-fingerprint): show fingerprint of an already known host
- [`stickimage`](stickimage): display an image always-on-top like a sticky note
- [`stfu`](stfu): fire and forget a command, run in background, discard stdout/stderr
- [`supybot-shell`](supybot-shell): Supybot plugin: execute shell commands and see their output
- [`su-with-args`](su-with-args): calls su(1) but uses arguments properly
- [`tailsleep`](tailsleep): like tail -f but quits when I/O activity stops
- [`trim-trailing-whitespace`](trim-trailing-whitespace): remove spaces, tabs and alike at end of each line
- [`uniq-unsorted`](uniq-unsorted): like uniq(1) but does not require lines to be sorted
- [`univisible`](univisible): tweak Unicode combinations and visualize them
- [`vhd`](vhd): visual hex dump, splitting at newlines, not fixed-width lines
- [`wakeonwan`](wakeonwan): wake remote machines with Wake-on-WAN
- [`wallpaper-curtain`](wallpaper-curtain): show an image with low-opacity on top of other windows
- [`xattrs-csv`](xattrs-csv): print a CSV of selected xattrs of selected files
- [`xattrs-filter`](xattrs-filter): filter a file list based on whether xattrs have desired values
- [`xattrs-set`](xattrs-set): set/unset xattrs on files with a nice command-line syntax
- [`xephyr-run-cmd`](xephyr-run-cmd): run a Xephyr server and run a command in it (like xvfb-run)
- [`yml2json`](yml2json): basic convert YAML to JSON
- [`zeropipe`](zeropipe): wrapper for other programs which can take NULL-separated lines

For more info, see also: http://indigo.re

## Licence

All code in this repository is licensed under the WTFPLv2. See COPYING.WTFPL.
