#!/bin/env bash
BASE_DIR=/home1/irteam/apps/calender
LOG_DIR=/home1/irteam/logs/calender

function shutdown()
{
    date
    echo "Shutting down calender"
    $BASE_DIR/oneapp.calender.ctl stop
}

# stop
trap shutdown HUP INT QUIT ABRT KILL ALRM TERM TSTP

# start
date
echo "Starting calender"
echo "$BASE_DIR/oneapp.calender.ctl start"
$BASE_DIR/oneapp.calender.ctl start

echo "Waiting for `cat $LOG_DIR/calender.pid` and `cat $LOG_DIR/nginx/nginx.pid`"
while [ -f $LOG_DIR/calender.pid ] && kill -0 `cat $LOG_DIR/calender.pid` && [ -f $LOG_DIR/nginx/nginx.pid ] && kill -0 `cat $LOG_DIR/nginx/nginx.pid`; do
    sleep 5
done
