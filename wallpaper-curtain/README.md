# wallpaper-curtain

Wallpaper-curtain shows an image with low-opacity on top of other windows
and desktop.

If you're sad not to see any wallpaper due to too many windows. You can display
a translucent image above everything.

## Usage

	wallpaper-curtain --opacity 0.25 /my/wallpaper.jpg

## Quitting

Since wallpaper-curtain has no window, it can't be closed easily.
Click the icon in system tray to quit it.

Else, kill the process with Ctrl-C or pkill:

	pkill -f wallpaper-curtain

## Dependencies

Requires Python3 and PyQt5.
