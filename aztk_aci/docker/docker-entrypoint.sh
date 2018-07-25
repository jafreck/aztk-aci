#!/bin/bash
set -e

echo "- Starting all Spark processes under supervisord"

export MASTER_IP="$2"

start_supervisord(){
    /usr/bin/supervisord --configuration /etc/supervisord.conf
}

if [ $1 == "worker" ]; then
    start_supervisord
    supervisorctl start worker 
fi
if [ $1 == "master" ]; then
    start_supervisord
    supervisorctl start master
fi

tail -F /dev/null
