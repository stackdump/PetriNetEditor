#!/usr/bin/env bash

if [[ "x${RDS_HOST}" = 'x'  && "x${RDS_PORT_5432_TCP_ADDR}" != "x" ]] ; then
    # map from docker ENV vars
    export RDS_HOST=${RDS_PORT_5432_TCP_ADDR}
fi

if [[ "x${AMQP_HOST}" = 'x' && "x${AMQP_PORT_5671_TCP_ADDR}" != "x" ]] ; then
    # map from docker ENV vars
    export AMQP_HOST=${AMQP_PORT_5671_TCP_ADDR}
fi

if [[ "x${PNML_PATH}" = 'x' ]] ; then
    export PNML_PATH=./schemata
fi

export PYTHONPATH=./
honcho start $@
