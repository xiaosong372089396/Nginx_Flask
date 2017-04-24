#!/bin/bash
wget -q -O - http://linux.dell.com/repo/hardware/latest/bootstrap.cgi | bash
yum install srvadmin-all
ln -s /opt/dell/srvadmin/sbin/omreport /usr/bin/omreport
ln -s /opt/dell/srvadmin/sbin/omconfig /usr/bin/omconfig
echo "/usr/bin/omconfig system webserver action=stop" >>/opt/dell/srvadmin/sbin/srvadmin-services.sh
/opt/dell/srvadmin/sbin/srvadmin-services.sh start
echo "/opt/dell/srvadmin/sbin/srvadmin-services.sh start">>/etc/rc.local
