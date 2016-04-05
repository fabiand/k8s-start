#!/bin/sh
set -x

grep -rl CONTROLLER_HOST /etc/nginx/nginx.conf | xargs sed -i "s#CONTROLLER_HOST#$CONTROLLER_PORT_8080_TCP_ADDR#g"
grep -rl CONTROLLER_PORT /etc/nginx/nginx.conf | xargs sed -i "s#CONTROLLER_PORT#$CONTROLLER_PORT_8080_TCP_PORT#g"
grep -rl ENGINE_HOST /etc/nginx/nginx.conf | xargs sed -i "s#ENGINE_HOST#$ENGINE_HOST#g"
grep -rl ENGINE_PORT /etc/nginx/nginx.conf | xargs sed -i "s#ENGINE_PORT#$ENGINE_PORT#g"
nginx -g 'daemon off;'
