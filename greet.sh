#!/bin/sh
# Print a greeting from quorum-sandbox, optionally addressed to a name.

if [ -n "$1" ]; then
  printf 'Hello, %s, from quorum-sandbox\n' "$1"
else
  printf 'Hello from quorum-sandbox\n'
fi
