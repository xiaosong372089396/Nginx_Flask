#! /bin/bash


pro="LoginGate"
port="5001"


while true
do
sleep 1
check=`netstat -ntlp|grep ${port}`

if [[ ${check} == "" ]];then
    cd /opt/CardServer/${pro}
      ./XL${pro}
     sleep 1
   if [ $? == 0 ];then
       echo "$(date +%F) ${pro} now is start " >> /opt/CardServer/watchdog.log
   else
       echo "$(date +%F) ${pro} startup failed " >> /opt/CardServer/watchdog.log
   fi
fi 
done
