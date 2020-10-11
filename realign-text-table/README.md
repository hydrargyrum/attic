# realign-text-table

`realign-text-table` redraws malformed ASCII-drawn tables

# Example

`realign-text-table` reads stdin or argument file.
When given this table as stdin:

    +-----+-----+
    | foo | bar |
    +-----+-----+
    | a long cell | short |
    | x | longer cell ? |
    +--+--+

it will output a well-formed table:

    +-------------+---------------+
    |     foo     |      bar      |
    +-------------+---------------+
    | a long cell |     short     |
    |      x      | longer cell ? |
    +-------------+---------------+

# Dependencies
`realign-text-table` uses Python and PrettyTable.
