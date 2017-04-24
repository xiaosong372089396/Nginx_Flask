#!/bin/bash

redmine=`ps -C ruby --no-header | wc -l`
if [ $redmine -eq 1 ];then
    echo "1"
elif [ $redmine -eq 0 ];then
    echo "0"
fi



