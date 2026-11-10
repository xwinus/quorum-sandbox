#!/bin/sh
# Print a greeting addressed to the first line of the file given as the only argument.
# Only LF ends a line; every other byte, a carriage return included, is part of the name.
# An empty file or an empty first line prints the default greeting.

if [ "$#" -ne 1 ]; then
  printf 'usage: greet-file.sh FILE\n' >&2
  exit 2
fi

file=$1

if [ -d "$file" ]; then
  printf 'greet-file.sh: cannot read FILE: %s: is a directory\n' "$file" >&2
  exit 1
fi

# Only a failed open is an error; read also fails at end of file, which is fine.
# (No `if !` here: bash as sh ignores the negation when the redirection fails.)
name=
{ IFS= read -r name || :; } 2>/dev/null <"$file" || {
  printf 'greet-file.sh: cannot read FILE: %s\n' "$file" >&2
  exit 1
}

if [ -n "$name" ]; then
  printf 'Hello, %s, from quorum-sandbox\n' "$name"
else
  printf 'Hello from quorum-sandbox\n'
fi
