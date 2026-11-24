#!/bin/sh
# Print a greeting, optionally addressed to the name given as the first argument.
# With --repeat {1|2|3} as the first arguments, print it that many times.

usage() {
  printf 'Usage: greet.sh --repeat {1|2|3} [NAME]\n' >&2
  exit 2
}

count=1
if [ "${1:-}" = '--repeat' ]; then
  case "${2:-}" in
    1 | 2 | 3) count=$2 ;;
    *) usage ;;
  esac
  [ "$#" -le 3 ] || usage
  shift 2
fi

while [ "$count" -gt 0 ]; do
  if [ -n "${1:-}" ]; then
    printf 'Hello, %s, from quorum-sandbox\n' "$1"
  else
    printf 'Hello from quorum-sandbox\n'
  fi
  count=$((count - 1))
done
