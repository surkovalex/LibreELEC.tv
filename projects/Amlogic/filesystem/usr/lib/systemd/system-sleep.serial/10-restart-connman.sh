#!/bin/sh

case $1 in
    post)
        systemctl restart connman
    ;;
esac
