#!/bin/bash

netstat -tnlp | grep LISTEN | awk '{print $4}' | awk -F\: '{print $2}' | grep -v ^$ > port.txt
total=`cat port.txt|wc -l`

echo '{'
echo '                "data":['
cc=1
for i in `cat port.txt`
do
             if [ $total -ne $cc ];then
                             echo   -n "
      "
                             echo   \{
                             echo   -n "
      "
                             echo   \"\{\#TCP_PORT\}\"\:\"$i\"\
}\,
             else
                             echo   -n "
"
                             echo   \{
                             echo   -n "
                   "
                             echo   \"\{\#TCP_PORT\}\"\:\"$i\"\
}\]\}
              fi
              ((cc++))
done

