# `yetictl` - Managing your Yeti server

Yeti ships with `yetctl`, a tiny CLI utility that can be used to manage a Yeti
server.

## Installation

Running `pipenv --install` automatically installs `yetictl` in your
`$PATH`. `yetictl` is just a shorthand to the `cli/yetictl.py` script::

    $ yetictl --help
    Usage: yetictl [OPTIONS] COMMAND [ARGS]...
    [...snip...]

    $ python cli/yetictl.py --help
    Usage: yetictl.py [OPTIONS] COMMAND [ARGS]...
    [...snip...]

## User management

User management is done with the `yetictl` script.

### Adding users

    $ yetictl add-user --help
    Usage: yetictl add-user [OPTIONS] USER_EMAIL

    Options:
    --password TEXT  Take password from CLI
    --admin          Give admin rights to this user
    --help           Show this message and exit.

Example::

    $ yetictl add-user admin@admin.com --admin
    Password:
    Repeat for confirmation:
    User admin@admin.com created succesfully (ID: 2489500)
    Admin: True
    API key: 9733e2c150319eaf54639d210ebf72647d9ba01bdd20209ea7ddff42026f7417

### Reseting user passwords

    $ yetictl reset-password --help
    Usage: yetictl reset-password [OPTIONS] USER_EMAIL

    Options:
    --password TEXT  Take password from CLI
    --help           Show this message and exit.

Example::

    $ yetictl reset-password admin@admin.com
    Password:
    Repeat for confirmation:
    User admin@admin.com created succesfully (ID: 2489500)
    Admin: True
    API key: 323ab22c0d4d0ead3884e1ee7bdda6daf995205c59e4d594e2d49b587bdb407d

## Populate kill-chains

This populates Yeti's database with default kill-chains. See file
`/cli/killchains.json` for details.

    $ yetictl killchain-import --help
    Usage: yetictl killchain-import [OPTIONS]

    Options:
    --killchain_filter TEXT  Filter on killchains to add
    --help                   Show this message and exit.

## Import TAXII collections

Yeti has built-in support for STIX 2 and TAXII feeds. Use the `taxii-import`
subcommand to import a given TAXII collection into Yeti::

    $ yetictl taxii-import --help
    Usage: yetictl taxii-import [OPTIONS]

    Options:
    --collection_url TEXT  Remote TAXII collection URL   [required]
    --help                 Show this message and exit.

Example::

    $ yetictl taxii-import --collection_url https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e/

## Populate vocabularies

This populates Yeti's database with default vocabularies. See file
`/cli/vocabs.json` for details::

    $ yetictl vocab-import --help
    Usage: yetictl vocab-import [OPTIONS]

    Options:
    --vocab_filter TEXT  Filter on vocabs to add
    --help               Show this message and exit.

## Launch Yeti's development webserver

Use this subcommand to launch a webserver exposing Yeti's API.

    $ yetictl webserver --help
    Usage: yetictl webserver [OPTIONS]

    Options:
    --debug           launch server in debug mode
    --interface TEXT  interface to listen on
    --port INTEGER    port to listen on
    --help            Show this message and exit.
