#!/bin/sh
envsubst '${LOCALHOST}' < /etc/nginx/conf.d/ft_transcendence.conf.template > /etc/nginx/conf.d/ft_transcendence.conf
nginx -g 'daemon off;'
