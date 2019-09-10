#!/bin/env bash

# supervisord and calender logs are auto cleaned.
# see the configure files for them.

# remove out of date calender logs and compress log
clover_log_path=/home1/irteam/logs/calender/
find $calender_log_path -mtime +50 -name 'calender.log.*.xz' -delete
find $calender_log_path -name 'calender.log.*-*' -not -name 'calender.log.*.xz' -execdir xz -z -T4 {} \;

# rotate and remove out of date nginx logs
nginx_log_path=/home1/irteam/logs/calender/nginx
post_fix=`date -d yesterday +%Y-%m-%d`
find $nginx_log_path -mtime +50 -name '*.xz' -delete
find $nginx_log_path -name 'access.log' -execdir mv {} {}.$post_fix \;
find $nginx_log_path -name 'error.log' -execdir mv {} {}.$post_fix \;
/home1/irteam/apps/calender/nginx/sbin/nginx -s reopen
find $nginx_log_path -name 'access.log.*' -not -name 'access.log.*.xz' -execdir xz -z -T4 {} \;
find $nginx_log_path -name 'error.log.*' -not -name 'error.log.*.xz' -execdir xz -z -T4 {} \;

