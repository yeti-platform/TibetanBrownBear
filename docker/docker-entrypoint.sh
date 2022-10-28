#!/bin/bash
set -e

PYTHONPATH="/app"

if [[ "$1" =~ "bootstrap" ]]; then
    poetry run /app/ctl/yetictl.py add-user admin@admin.com --password admin
    poetry run /app/ctl/yetictl.py taxii-import --collection_url https://cti-taxii.mitre.org/stix/collections/2f669986-b40b-4423-b720-4396ca6a462b/
    poetry run /app/ctl/yetictl.py taxii-import --collection_url https://cti-taxii.mitre.org/stix/collections/062767bd-02d2-4b72-84ba-56caef0f8658/
    poetry run /app/ctl/yetictl.py taxii-import --collection_url https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e/
    poetry run /app/ctl/yetictl.py mitre-tactics-import
    poetry run /app/ctl/yetictl.py vocab-import
    poetry run /app/ctl/yetictl.py killchain-import
fi

if [[ "$1" =~ "webserver" ]]; then
    exec poetry run /app/ctl/yetictl.py webserver
fi

exec "$@"
