#!/bin/sh
# Print a greeting for every line of the file given as the only argument.
# Only LF ends a line; every other byte, a carriage return included, is part of the name.
# A final line without LF is still greeted; an empty line prints the default greeting.

if [ "$#" -ne 1 ]; then
  printf 'usage: greet-list.sh FILE\n' >&2
  exit 2
fi

file=$1

if [ -d "$file" ]; then
  printf 'greet-list.sh: cannot read FILE: %s: is a directory\n' "$file" >&2
  exit 1
fi

# The block runs only once the file is open, so an unset `opened` means the open failed.
# (No `if !` or `||` on the block: its status is also that of the last greeting.)
opened=
{
  opened=1
  # read fails at end of file, but still sets name to a final line without LF.
  while IFS= read -r name || [ -n "$name" ]; do
    if [ -n "$name" ]; then
      printf 'Hello, %s, from quorum-sandbox\n' "$name"
    else
      printf 'Hello from quorum-sandbox\n'
    fi
  done
} 2>/dev/null <"$file"

if [ -z "$opened" ]; then
  printf 'greet-list.sh: cannot read FILE: %s\n' "$file" >&2
  exit 1
fi
