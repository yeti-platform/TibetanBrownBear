# Yeticli - the Yeti CLI

Yeti ships with `yeticli`, a tiny CLI utility that offers wrappers around
common tasks that leverage Yeti's HTTP API.

## Installation

Running `pipenv --install` automatically installs `yeticli` in your
`$PATH`. `yeticli` is just a shorthand to the `cli/yetictl.py` script::

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

## User management

User management is done with the `yeticli` script.

### Adding users

    $ yeticli add-user --help
    Usage: yeticli add-user [OPTIONS] USER_EMAIL

    Options:
    --password TEXT  Take password from CLI
    --admin          Give admin rights to this user
    --help           Show this message and exit.

Example::

    $ yeticli add-user admin@admin.com --admin
    Password:
    Repeat for confirmation:
    User admin@admin.com created succesfully (ID: 2489500)
    Admin: True
    API key: 9733e2c150319eaf54639d210ebf72647d9ba01bdd20209ea7ddff42026f7417

### Reseting user passwords

    $ yeticli reset-password --help
    Usage: yeticli reset-password [OPTIONS] USER_EMAIL

    Options:
    --password TEXT  Take password from CLI
    --help           Show this message and exit.

Example::

    $ yeticli reset-password admin@admin.com
    Password:
    Repeat for confirmation:
    User admin@admin.com created succesfully (ID: 2489500)
    Admin: True
    API key: 323ab22c0d4d0ead3884e1ee7bdda6daf995205c59e4d594e2d49b587bdb407d

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
