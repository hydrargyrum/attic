# ffmcut

Use ffmpeg to cut a video

# Synopsis

	ffmcut INPUT START END OUTPUT

# Description

Cut INPUT video file from START timestamp to END timestamp and write OUTPUT file.

START and END arguments are in seconds but minutes and hours are also supported. Examples:

	30
	10:30
	1:20:00

# Example

	ffmcut infile.avi 10:25 10:30 outfile.avi
