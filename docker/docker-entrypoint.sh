#!/bin/bash
set -e

if [ "$1" = 'webserver' ]; then
    exec python3 /opt/yeti/yetictl webserver
fi

exec "$@"
