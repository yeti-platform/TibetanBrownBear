#!/bin/bash
set -e

PYTHONPATH="/opt/yeti"

if [ "$1" =~ "bootstrap" ]; then
    python3 /opt/yeti/ctl/yetictl.py taxii-import --collection_url https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e/
    python3 /opt/yeti/ctl/yetictl.py mitre-taxii-import
    python3 /opt/yeti/ctl/yetictl.py vocab-import
    python3 /opt/yeti/ctl/yetictl.py killchain-import
    python3 /opt/yeti/ctl/yetictl.py add-user admin@admin.com
fi

if [ "$1" =~ "webserver" ]; then
    exec python3 /opt/yeti/ctl/yetictl.py webserver
fi

exec "$@"
