#!/bin/bash
config='/usr/share/denyhosts/denyhosts.cfg'
home=`pwd`
if [ -s DenyHosts-2.6.tar.gz ]; then
  echo "DenyHosts-2.6.tar.gz [found]"
  else
  exit 1
fi

tar zxvf DenyHosts-2.6.tar.gz
cd DenyHosts-2.6
python setup.py install

cd /usr/share/denyhosts/
cp denyhosts.cfg-dist denyhosts.cfg
panduan=`cat /usr/share/denyhosts/denyhosts.cfg | grep "PURGE_DENY = 1d" | wc -l`
if [ $panduan == 1 ]; then
 echo "config file has been fixed"
 exit 1
 else
 sed -i 's/PURGE_DENY =/PURGE_DENY = 1d/g' $config
 sed -i 's/DENY_THRESHOLD_ROOT = 1/DENY_THRESHOLD_ROOT = 5/g' $config
 sed -i 's/HOSTNAME_LOOKUP=YES/HOSTNAME_LOOKUP=NO/g' $config
 sed -i 's/DAEMON_PURGE = 1h/DAEMON_PURGE = 1d/g' $config
fi

cd /usr/share/denyhosts
cp daemon-control-dist daemon-control
chown root daemon-control
chmod 700 daemon-control
ln -s /usr/share/denyhosts/daemon-control /etc/init.d/denyhosts
/etc/init.d/denyhosts start
chkconfig denyhosts on
