<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/senseit-logo-inverse.svg">
    <img alt="senseIT" src="assets/logo/senseit-logo.svg" width="360">
  </picture>
</p>

# quorum-sandbox

## Usage

```sh
sh greet.sh
# Hello from quorum-sandbox

sh greet.sh Vaclav
# Hello, Vaclav, from quorum-sandbox

sh greet.sh --repeat 2 Vaclav
# Hello, Vaclav, from quorum-sandbox
# Hello, Vaclav, from quorum-sandbox
```

`--repeat` must be the first argument and accepts only the counts 1, 2 or 3. An invalid count or more than one name prints the usage line to stderr and exits with code 2.
