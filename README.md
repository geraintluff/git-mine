# git-mine

Python script that amends Git's current HEAD to minimise

## Usage:

The only argument is the limit (in hex) below which the tool will exit.

```
./git-mine.py 000001
```

This will exit when the commit ID for HEAD starts `000000...`

If the limit is omitted, then it defaults to `0001` (first 16 bytes zeros).

The limit is a lexical comparison on the hex representation - to continue infinitely, specify `-` as the limit.

## Use as `post-commit` hook

You can add a post-commit hook in git that calls this with a preset limit, to make sure that all your commits stay below a certain threshhold.

To do this, create the script `.git/hooks/post-commit` (must be executable) with the contents:

```
#!/bin/bash
/location/to/git-mine.py 0001
```
