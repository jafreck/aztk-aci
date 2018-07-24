#!/bin/bash
set -e

echo "- Starting Spark master under supervisord"

export MASTER_IP="$2"

start_supervisord(){
    /usr/bin/supervisord --configuration /etc/supervisord.conf
}

start_supervisord
supervisorctl start master


tail -F /dev/null
