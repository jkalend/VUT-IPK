#!/bin/bash

echo $MODE $HOST $PORT
echo "Starting ipkpd with mode ${MODE:-tcp} on port and host ${HOST:-0.0.0.0}:${PORT:-2023}"

RET=1
until [ $RET -eq 0 ]; do
    ./ipkpd -p ${PORT:-2023} -h ${HOST:-0.0.0.0} -m ${MODE:-tcp}
    echo "ipkpd crashed with exit code $?. Respawning.." >&2
done

echo "ipkpd exited with code $?"
