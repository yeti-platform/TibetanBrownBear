# `yeticli` - the Yeti CLI

Yeti ships with `yeticli`, a tiny CLI utility that offers wrappers around
common tasks that leverage Yeti's HTTP API.

## Installation

Running `pipenv --install` automatically installs `yeticli` in your
`$PATH`. `yeticli` is just a shorthand to the `cli/yeticli.py` script::

    $ yeticli --help
    Usage: yeticli [OPTIONS] COMMAND [ARGS]...
    [...snip...]

    $ python cli/yeticli.py --help
    Usage: yeticli.py [OPTIONS] COMMAND [ARGS]...
    [...snip...]

## Getting help

`yeticli` has a handy help menu::

    $ yeticli --help
    Usage: yeticli [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    dump-yara-rules  Dump existing Yara rules to files in a local directory.
    match            Matches a string or a file's contents against all yeti...
    yara-scan        Scan a local file or directory using Yara rules from the...

To get more details on a specific sub-command, just run `yeticli <SUBCOMMAND> --help`::

    $ yeticli match --help
    Usage: yeticli match [OPTIONS]

    Matches a string or a file's contents against all yeti Indicators.

    Options:
    --verbose        Display match details
    --filename TEXT  Upload a file to be matched instead.
    --string TEXT    String against which to match indicators.
    --help           Show this message and exit.
