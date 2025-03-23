# tailsleep #

tailsleep is a command-line program that reads a file and prints its content to stdout, and if the file is modified externally by appending data, the new data is written to stdout. However, if the file is not modified within a few seconds (5 seconds by default), tailsleep exits.

It is a bit like the "`tail -f`" command (hence the name) but it writes the full content of the file (not the 10 last lines), and exits when the file is not modified for some time.

# Sample uses #

Extract a file that is being downloaded by a web browser:

```
tailsleep file-being-downloaded.tar.gz.part | tar -xzf -
```

As an extension, download Flash videos loading/loaded in your web browser (doesn't need to be playing them, they can be paused):

```
find /proc/*/fd -lname "*FlashXX*" | while read -r vid
do
	tailsleep $vid > "video-`basename $vid`.flv"
done
```
