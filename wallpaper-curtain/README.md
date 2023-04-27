# wallpaper-curtain

Wallpaper-curtain shows an image with low-opacity on top of other windows
and desktop.

If you're sad not to see any wallpaper due to too many windows. You can display
a translucent image above everything.

This can also be used in your `crontab` to stop you from remote working outside
of office hours, see below.

## Usage

	wallpaper-curtain --opacity 0.25 /my/wallpaper.jpg

## Quitting

Since wallpaper-curtain has no window, it can't be closed easily.
Click the icon in system tray to quit it.

Else, kill the process with Ctrl-C or pkill:

	pkill -f wallpaper-curtain

## Example

Display a red curtain over every window when outside office hours

	# generate the red curtain
	convert -size 4000x4000 xc:red ~/redbox.png

	# add this to `crontab -e`
	0 7 * * 1-5 pkill -f wallpaper-curtain
	0 19 * * 1-5 DISPLAY=:0 wallpaper-curtain -o 0.7 ~/redbox.png

This does not prevent using the session, it's a more kind of warning.
Hardlocking accounts can be done with /etc/security/time.conf

## Dependencies

Requires Python3 and PyQt6, and a compositing window manager for translucency to work.
