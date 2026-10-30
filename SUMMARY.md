# Summary: qrm-a9sey9: add a greeting script with an optional name

## What changed and why

- `greet.sh` (new, at the repository root): a POSIX `sh` script so the repository has something runnable.
  With no argument it prints `Hello from quorum-sandbox`. With a non-empty first argument it prints
  `Hello, <name>, from quorum-sandbox`. It uses `printf '%s'`, so a name containing `%` or `-n` is
  printed literally.
- `README.md`: added a "Usage" section showing both invocations and their output.
- `QUESTIONS.md`: lists the open questions and the guesses I proceeded on.

## Acceptance criteria

| Criterion | How it is met | Verified by |
|---|---|---|
| `sh greet.sh` prints `Hello from quorum-sandbox` and exits 0 | `else` branch of `greet.sh` | `[ "$(sh greet.sh)" = "Hello from quorum-sandbox" ]` passed; exit code 0 |
| `sh greet.sh Vaclav` prints `Hello, Vaclav, from quorum-sandbox` | `if [ -n "$1" ]` branch | `[ "$(sh greet.sh Vaclav)" = "Hello, Vaclav, from quorum-sandbox" ]` passed; exit code 0 |
| `README.md` has a short "Usage" section showing both invocations | New `## Usage` section | Reviewed manually |

## Assumptions (see `QUESTIONS.md`)

- An empty first argument (`sh greet.sh ""`) is treated as no name.
- Only the first argument is used. `./greet.sh Ada Lovelace` prints `Hello, Ada, from quorum-sandbox`.
- No test harness was added: the repository has none, and the issue puts other build tooling out of scope.
  The criteria were checked by running the script directly (commands below).

## Not done

- There are no automated tests in the repository, so none were added (see above).
- I did not commit `.quorum-skill.md`. It was untracked when the session started and is not part of the issue.

## Commands run and final results

```sh
sh greet.sh                      # before implementing: "No such file or directory", exit 127
sh greet.sh                      # Hello from quorum-sandbox            exit=0
sh greet.sh Vaclav               # Hello, Vaclav, from quorum-sandbox   exit=0
sh greet.sh ""                   # Hello from quorum-sandbox            exit=0
sh greet.sh '%s -n'              # Hello, %s -n, from quorum-sandbox    exit=0
./greet.sh Ada Lovelace          # Hello, Ada, from quorum-sandbox      exit=0
dash greet.sh Vaclav             # Hello, Vaclav, from quorum-sandbox
[ "$(sh greet.sh)" = "Hello from quorum-sandbox" ] && \
  [ "$(sh greet.sh Vaclav)" = "Hello, Vaclav, from quorum-sandbox" ] && echo EXACT-MATCH-OK   # EXACT-MATCH-OK
shellcheck greet.sh              # no findings
```

## Note on pushing

`git push quorum HEAD:quorum/qrm-a9sey9` alone failed in this worktree:

1. The runner's credential helper only returns a token when git sends a `path=gateway/...` field.
   Git sends `path` only when `credential.useHttpPath` is true, and that setting is not configured.
2. The system-wide `osxkeychain` helper runs first. It stored the one-shot token after the first
   successful push and then kept returning it, so later pushes got
   `403 token is not valid for this repository`.

Every push used the same remote and refspec, with config set for that command only (no repository
config or remote was changed):

```sh
H="$(git config --local credential.helper)"
git -c credential.helper= -c "credential.helper=$H" -c credential.useHttpPath=true \
  push quorum HEAD:quorum/qrm-a9sey9
```

The keychain still holds one stale token for `127.0.0.1:7400/gateway/github:1439746995`. It was
left in place because it is outside this working directory.
