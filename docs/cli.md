# Yeticli - the Yeti CLI

Yeti ships with `yeticli`, a tiny CLI utility that offers wrappers around
common tasks that leverage Yeti's HTTP API.

## Installation

Running `pipenv --install` automatically installs `yeticli` in your
`$PATH`. `yeticli` is just a shorthand to the `/cli/yetictl.py` script::

    $ yeticli --help
    Usage: yeticli [OPTIONS] COMMAND [ARGS]...
    [...snip...]

    $ python cli/yetictl.py --help
    Usage: yetictl.py [OPTIONS] COMMAND [ARGS]...
    [...snip...]

## Getting help

`yeticli` has a handy help menu::

    $ yeticli --help
    Usage: yeticli [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    killchain-import
    taxii-import
    vocab-import
    webserver

To get more details on a specific sub-command, just run `yeticli <SUBCOMMAND> --help`::

    $ yeticli taxii-import --help
    Usage: yeticli taxii-import [OPTIONS]

    Options:
    --collection_url TEXT  Remote TAXII collection URL   [required]
    --help                 Show this message and exit.


## Populate kill-chains

This populates Yeti's database with default kill-chains. See file
`/cli/killchains.json` for details.

    $ yeticli killchain-import --help
    Usage: yeticli killchain-import [OPTIONS]

    Options:
    --killchain_filter TEXT  Filter on killchains to add
    --help                   Show this message and exit.

## Import TAXII collections

Yeti has built-in support for STIX 2 and TAXII feeds. Use the `taxii-import`
subcommand to import a given TAXII collection into Yeti::

    $ yeticli taxii-import --help
    Usage: yeticli taxii-import [OPTIONS]

    Options:
    --collection_url TEXT  Remote TAXII collection URL   [required]
    --help                 Show this message and exit.

Example::

    $ yeticli taxii-import --collection_url https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e/

## Populate vocabularies

This populates Yeti's database with default vocabularies. See file
`/cli/vocabs.json` for details::

    $ yeticli vocab-import --help
    Usage: yeticli vocab-import [OPTIONS]

    Options:
    --vocab_filter TEXT  Filter on vocabs to add
    --help               Show this message and exit.

## Launch Yeti's development webserver

Use this subcommand to launch a webserver exposing Yeti's API.

    $ yeticli webserver --help
    Usage: yeticli webserver [OPTIONS]

    Options:
    --debug           launch server in debug mode
    --interface TEXT  interface to listen on
    --port INTEGER    port to listen on
    --help            Show this message and exit.