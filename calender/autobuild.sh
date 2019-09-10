#!/bin/env bash
cd externals
ls *.gz | xargs -I {} tar xzf {}
cd nginx-1.13.7
./configure --add-module= --with-pcre=../pcre-8.41 --with-zlib=../zlib-1.2.11 --with-openssl=../openssl-1.1.0g --with-http_gzip_static_module --with-http_stub_status_module --prefix=/home1/irteam/apps/calender/nginx --with-http_ssl_module 
make -j4
make install
cd ../..
cp conf/nginx.conf /home1/irteam/apps/calender/nginx/conf/
mkdir -p tmp
mkdir -p /home1/irteam/logs/calender/nginx
mkdir -p /home1/irteam/logs/supervisord/calender
