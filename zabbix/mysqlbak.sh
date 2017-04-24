#/bin/bash
#-*- coding:utf-8 -*-
user=zabbix
userPWD=zabbix
dbNames=(zabbix)
dataBackupDir=/server/script
eMailFile=$dataBackupDir/log/email.txt
eMail=xxxxxxxx@139.com
logFile=$dataBackupDir/log/mysqlbackup.log
DATE=`date -d "now" +%Y%m%d`
echo `date -d "now" "+%Y-%m-%d %H:%M:%S"` > $eMailFile

for Zabbix in ${dbNames[*]}
do
#参考说明：http://www.cnblogs.com/wxb-km/p/3610594.html
#--skip-opt :在转储结果前将整个结果集装入内存。如果转储大数据库可能会出现问题，该选项默认启用，但可以用--skip-opt禁用
#--create-option : 在CREATE TABLE语句包含所有MySQL表选项
#--set-charset : 将SET NAMES default_character_set加到输出中。该选项默认启用。要想禁用SET NAMES语句，使用--skip-set-charset
#--default-character-set=utf8: 使用charsetas默认字符集。如果没有指定，mysqldump使用utf8
#--max_allowed_packet: 客户端/服务器之间通信的缓存区的最大大小。最大为1GB：
#--net_buffer_length: 客户端/服务器之间通信的缓存区的初始大小。当创建多行插入语句时(如同使用选项--extended-insert或--opt)，mysqldump创建长度达net_buffer_length的行。如果增加该变量，还应确保在MySQL服务器中的net_buffer_length变量至少这么大。
mysqldump  -u$user -p$userPWD $Zabbix --skip-opt --create-option --set-charset --default-character-set=utf8 -e --max_allowed_packet=132000000 --net_buffer_length=16380 | gzip > /server/script/$Zabbix-$DATE.sql.gz
done

if [[ $? == 0 ]]; then
    echo "Zabbix Database Backup Success!" >> $eMailFile
else
    echo "Zabbix Database Backup Fail!" >> $eMailFile
fi

echo "====================================" >> $logFile
cat $eMailFile >> $logFile
echo $dumpFile >> $logFile
