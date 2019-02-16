#!/bin/bash
set -e

PYTHONPATH="/opt/yeti"

echo '### Yeti docker entrypoint ###'
echo -n 'Command: '
echo $1

if [ "$1" = 'webserver' ]; then
    exec python3 /opt/yeti/ctl/yetictl.py webserver
fi

if [ "$1" = 'taxii-mitre' ]; then
    exec python3 /opt/yeti/ctl/yetictl.py taxii-import --collection_url https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e/
fi

echo "Command $@ not found."
exec python3 /opt/yeti/ctl/yetictl.py "$@"
