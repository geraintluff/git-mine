# git-mine

Python script that amends Git's current HEAD to minimise

## Usage:

The only (optional) argument is the limit (in hex) below which the tool will exit.

```
./git-mine.py 000001
```

This will exit when the commit ID for HEAD starts `000000...`

If the limit is omitted, then it will mine until it is interrupted (CTRL+C).
