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
```

## Greeting arguments

`greet.sh` accepts one positional name. An empty name uses the default greeting.
Names are literal: `sh greet.sh --help` prints `Hello, --help, from quorum-sandbox`;
there is no option parser or help flag. Percent characters in names are literal too.
