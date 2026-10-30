# Questions for qrm-a9sey9

1. **How should an empty first argument (`sh greet.sh ""`) behave?**
   Best guess: treat it like no argument and print `Hello from quorum-sandbox`.
   Proceeding on the guess.

2. **Should a test harness be added?** The repository has no test setup, and the
   issue puts other build tooling out of scope.
   Best guess: do not add a test framework or test files; verify the acceptance
   criteria by running the script directly and record the commands in `SUMMARY.md`.
   Proceeding on the guess.

3. **Should arguments beyond the first be used (e.g. `sh greet.sh Ada Lovelace`)?**
   Best guess: no, only the first argument is used, as the issue states.
   Proceeding on the guess.
