#!/bin/env bash
env="alpha"
update="update"
if [ $# -gt 0 ];
then
  env=$1
fi

if [ $# -gt 1 ];
then
  update=$2
fi
echo $env" "$update

echo `python scripts/registerBot.py --env $env --update $update`
echo `python scripts/uploadContent.py --env $env --update $update`
echo `cp scripts/common.py calender/constants/`


