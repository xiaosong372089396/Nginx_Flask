#!/bin/bash

#install nagios-plugins
/usr/sbin/useradd nagios -s /sbin/nologin
cd /root/bash
tar zxvf /root/bash/nagios-plugins-2.0.tar.gz
cd /root/bash/nagios-plugins-2.0
./configure
make
make install
chown nagios:nagios /usr/local/nagios
chown -R nagios:nagios /usr/local/nagios/libexec

#install nrpe
cd /root/bash
tar zxvf nrpe-2.14.tar.gz
cd nrpe-2.14
./configure
make all
make install-plugin
make install-daemon
make install-daemon-config
