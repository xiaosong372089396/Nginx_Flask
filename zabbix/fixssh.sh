#!/bin/bash
fix=`more /etc/ssh/sshd_config | grep "PasswordAuthentication no" | wc -l`
if [ $fix == 2 ];then
  echo "sshd_config has been fixed"
 else
   sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/g' /etc/ssh/sshd_config
   sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
   sed -i 's/#RSAAuthentication yes/RSAAuthentication yes/g' /etc/ssh/sshd_config
   sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
   sed -i 's/#AuthorizedKeysFile/AuthorizedKeysFile/' /etc/ssh/sshd_config
   sed -i 's/#StrictModes yes/StrictModes no/g' /etc/ssh/sshd_config
   sed -i 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/sshd_config
fi
