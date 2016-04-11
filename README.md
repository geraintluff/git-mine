# git-mine

Python script that amends Git's current HEAD to minimise the commit ID

## Usage:

The only argument is the limit (in hex) below which the tool will exit.

```
./git-mine.py 000001
```

This will exit when the commit ID for HEAD starts `000000...`

If the limit is omitted, then it defaults to `0001` (first 16 bytes zeros).

The limit is a lexical comparison on the hex representation - to continue infinitely, specify `-` as the limit.

## Use as `post-commit` hook

If you'd like this script to run after every commit, copy `git-mine.py` into the file `.git/hooks/post-commit`.  It must be marked as executable.

If you want to specify a limit other than the default, you can write a script for `.git/hooks/post-commit` (must be executable) that provides it:

```
#!/bin/bash
/location/to/git-mine.py 0001
```

Alternatively, you could just change `DEFAULT_LIMIT` in the source.
