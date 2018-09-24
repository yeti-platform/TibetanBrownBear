#!/bin/bash
set -e

if [ "$1" = 'webserver' ]; then
    exec yeticli webserver
fi

if [ "$1" = 'taxii' ]; then
    exec yeticli taxii_import --collection_url https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e/
fi

exec "$@"
