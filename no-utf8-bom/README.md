# no-utf8-bom

UTF-8 has no byte order, so the so-called UTF-8 BOM is pointless.
Furthermore, it's always the same 3 futile bytes.

This tool just removes the UTF-8 BOM if present.

## Usage

    no-utf8-bom

Just operate on stdin and use stdout.

    no-utf8-bom [-i] FILE

Operate on FILE and use stdout.
If `-i` is given, modify FILE in place (and don't touch stdout).
