#!/bin/bash
set -e

echo "This is the docker entrypoint!"

if [ "$1" = 'webserver' ]; then
    exec python3 /opt/yeti/yetictl
fi

exec "$@"
