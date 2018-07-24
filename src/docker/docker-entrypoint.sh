#!/bin/bash
set -e

echo "- Starting all Spark processes under supervisord"


start_supervisord(){
    /usr/bin/supervisord --configuration /etc/supervisord.conf
}

if [ $1 == "worker" ]; then
    export MASTER_IP=$2
    start_supervisord
    supervisorctl -n start worker 
fi
if [ $1 == "master" ]; then
    start_supervisord
    supervisorctl -n start master
fi
