#!/bin/bash


#tcp status
tcp=$1
tmp_file=/tmp/tcp_status.txt
/bin/netstat -an|awk '/^tcp/{++S[$NF]}END{for(a in S) print a,S[a]}' > $tmp_file
 
case $tcp in
   CLOSED)
          output=$(awk '/CLOSED/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
   LISTEN)
          output=$(awk '/LISTEN/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
   SYN_RECV)
          output=$(awk '/SYN_RECV/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
   SYN_SENT)
          output=$(awk '/SYN_SENT/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
   ESTABLISHED)
          output=$(awk '/ESTABLISHED/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
   TIME_WAIT)
          output=$(awk '/TIME_WAIT/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
   CLOSING)
          output=$(awk '/CLOSING/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
   CLOSE_WAIT)
          output=$(awk '/CLOSE_WAIT/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
        ;;
   LAST_ACK)
          output=$(awk '/LAST_ACK/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
         ;;
   FIN_WAIT1)
          output=$(awk '/FIN_WAIT1/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
         ;;
   FIN_WAIT2)
          output=$(awk '/FIN_WAIT2/{print $2}' $tmp_file)
          if [ "$output" == "" ];then
             echo 0
          else
             echo $output
          fi
         ;;
         *)
          echo -e "\e[033mUsage: sh  $0 [CLOSED|CLOSING|CLOSE_WAIT|SYN_RECV|SYN_SENT|FINWAIT1|FINWAIT2|LISTEN|ESTABLISHED|LASTACK|TIME_WAIT]\e[0m"
   
esac
