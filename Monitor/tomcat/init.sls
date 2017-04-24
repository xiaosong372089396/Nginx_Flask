jdksource:
  file.managed:
    - name: /root/bash/jdk-7u55-linux-x64.rpm
    - source: salt://tomcat/jdk-7u55-linux-x64.rpm
    - user: root
    - group: root
    - mode: 644

bash_profile:  
  file.managed:
    - name: /root/.bash_profile
    - source: salt://tomcat/.bash_profile
    - user: root
    - group: root
    - mode: 644
  cmd.run:
    - name: source /root/.bash_profile

tomcat7:  
  file.managed:
    - name: /root/bash/apache-tomcat-7.0.52.tar.gz
    - source: salt://tomcat/apache-tomcat-7.0.52.tar.gz
    - user: root
    - group: root
    - mode: 755
  cmd.run:
    - cwd: /root/bash
    - names:
      - rpm -ivh jdk-7u55-linux-x64.rpm
      - tar zxvf apache-tomcat-7.0.52.tar.gz
      - mv apache-tomcat-7.0.52 /usr/local/tomcat7
      - sh /usr/local/tomcat7/bin/startup.sh

tomcat_shell: 
  file.managed:
    - name: /etc/init.d/tomcat
    - source: salt://tomcat/tomcat
    - user: root
    - group: root
    - mode: 755

  service.running:
    - enable: True
    - reload: True
    - watch:
      - file: tomcat_shell


