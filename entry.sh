#!/usr/bin/env bash

if [[ -f ./env.rc ]] ; then
    source env.rc
fi

pkill twistd 2>/dev/null

twistd $TWISTD_OPTS brython --listen-ip=0.0.0.0 --listen-port=8080

if [[ "${HOSTNAME}x" != "x" ]] ; then
    echo -n "http://${HOSTNAME}:8080 pid:"
    cat *.pid
    echo
fi
