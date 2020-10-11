# qunpak

Extract and list Quake .pak archive files.

```
qunpak PAK0.PAK
```

will extract PAK0.PAK.

It's also possible to simply list its content:

```
qunpak -l PAK0.PAK
```

Only some files can be extracted by specifying a glob-pattern ("*" will match slashes and dots):

```
qunpak PAK0.PAK "*.wav"
```

will extract all .wav files from the root content in PAK0.PAK.

By default, files are extracted in current directory, but another directory can be used:

```
qunpak -O /other/dir/where/to/extract PAK0.PAK
```
