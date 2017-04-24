

yum -y install make ncurses-devel gcc gcc-c++ unixODBC unixODBC-devel openssl openssl-devel

wget http://erlang.org/download/otp_src_19.1.tar.gz

tar xf otp_src_19.1.tar.gz
cd otp_src_19.1


./configure  --prefix=/usr/local/erlang --enable-smp-support --enable-threads --enable-sctp --enable-kernel-poll --enable-hipe --with-ssl


 make && make install

vim /etc/profile

ERL_HOME=/usr/local/erlang
PATH=$ERL_HOME/bin:$PATH
export ERL_HOME PATH

yum install xmlto -y

wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.6.6/rabbitmq-server-generic-unix-3.6.6.tar.xz
tar xf rabbitmq-server-generic-unix-3.6.6.tar.xz
mv rabbitmq_server-3.6.6 rabbitmq


vim /etc/profile

export PATH=$PATH:/opt/rabbitmq/sbin


./rabbitmqctl status
./rabbitmqctl stop
./rabbitmq-plugins enable rabbitmq_management

useradd admin
rabbitmqctl add_user admin
rabbitmqctl add_user admin xianlai
rabbitmqctl set_user_tags admin administrator




