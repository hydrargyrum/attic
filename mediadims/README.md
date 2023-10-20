# mediadims

Get audio/video duration or video width/height of a file with [mediainfo](https://mediaarea.net/).

## Examples

### Get duration in seconds (floating point) of an audio or video file

```
% mediadims duration somefile.mp3
142.30
```

### Get dimensions of a video file

```
% mediadims width somefile.avi
1280
```

```
% mediadims height somefile.avi
720
```

```
% mediadims wxh somefile.avi
1280x720
```

## Why merely wrap mediainfo?

All the heavy work of parsing audio/video files is done thanks to [mediainfo](https://mediaarea.net/) which is very powerful.
Unfortunately, its command-line interface is awkward (to say the least), so a wrapper is useful to make it more convenient.
Hence `mediadims`.

## Requirements

- python3
- [mediainfo](https://mediaarea.net/) command-line tool
