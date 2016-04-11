# git-mine

Python script that amends Git's current HEAD to minimise

## Usage:

The only (optional) argument is the limit (in hex) below which the tool will exit.

```
./git-mine.py 000001
```

This will exit when the commit ID for HEAD starts `000000...`

If the limit is omitted, then it will mine until it is interrupted (CTRL+C).

## Use as `post-commit` hook

You can add a post-commit hook in git that calls this with a given limit e.g.

```
#!/bin/bash
/location/to/git-mine.py 0001
```

This should be an executable file placed in `.git/hooks/post-commit`.
