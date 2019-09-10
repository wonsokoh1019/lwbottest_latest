#!/bin/env bash

name_of_self=$(basename ${0})
path_to_self=$(dirname ${0})
abspath_to_self=$(cd $path_to_self; pwd)
log_path=/home1/irteamsu/logs/calender
calender_pid_file=${log_path}/calender.pid
nginx_pid_file=${log_path}/nginx/nginx.pid
selfhealing_stop_file=/tmp/selfhealing.stop
cd ${abspath_to_self}

export PATH=/home1/irteamsu/miniconda3/bin:$PATH

case "${1}" in
    start)
        calender_started=0
        nginx_started=0
        if [ -e $calender_pid_file ]; then
            ps `cat $calender_pid_file`
            if [ $? -eq 0 ] ; then
                echo "already running!!"
                calender_started=1
            else
                rm $calender_pid_file #invalid pid_file
            fi
        fi

        if [ -e $nginx_pid_file ]; then
            ps `cat $nginx_pid_file`
            if [ $? -eq 0 ] ; then
                echo "ngxin already running!!"
                nginx_started=1
            else
                rm $nginx_pid_file
            fi
        fi

        if [ $calender_started -eq 0 ] ; then
            pkill -2 python3 #make sure children are not running
            sleep 3
            python3 ${abspath_to_self}/main.py --daemonize True
        fi
        if [ $nginx_started -eq 0 ] ; then
            pkill -9 nginx
            ${abspath_to_self}/nginx/sbin/nginx
        fi
    
        started=0
        for i in `seq 1 20`;
        do
            if [ -e $calender_pid_file ] && [ -e $nginx_pid_file ] ; then
                rm -f ${selfhealing_stop_file}
                touch ${abspath_to_self}/l7check.nhn
                started=1
                break
            fi
            sleep 1
        done
        
        if [ $started -eq 0 ] ; then
            echo "fail to start!"
            exit 1
        fi
        ;;
    stop)
        ps `cat $calender_pid_file`
        
        if [ $? -eq 0 ] ; then
            rm -f ${abspath_to_self}/l7check.nhn
            sleep 15
            touch ${selfhealing_stop_file}
           
            kill -2 `cat $calender_pid_file` 
            ${abspath_to_self}/nginx/sbin/nginx -s stop
        else
            echo "no live daemon to stop..."
            exit 1
        fi

        echo "stopped..."
        ;;
    *)
        echo "Usage: ${name_of_self} <start | stop>"
        exit 1
        ;;
esac

