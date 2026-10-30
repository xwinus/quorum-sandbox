#!/bin/sh
# Print a greeting, optionally addressed to the name given as the first argument.

if [ -n "${1:-}" ]; then
  printf 'Hello, %s, from quorum-sandbox\n' "$1"
else
  printf 'Hello from quorum-sandbox\n'
fi
