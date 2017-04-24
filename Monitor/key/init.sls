zabbix_agent:
  pkg.installed:
    - pkgs:
      - zabbix
      - zabbix-agent

  service:
    - name: zabbix-agent
    - running
    - enable: True
    - required:
      - pkgs:
        - zabbix
        - zabbix-agent
    - reload: True
    - watch:
      - file: /etc/zabbix/zabbix_agentd.conf

/etc/zabbix/zabbix_agentd.conf:
  file.managed:
    - source: salt://key/zabbix_agentd.conf
    - user: root
    - group: root
    - mode: 644

/tmp/port.sh:
  file.managed:
    - source: salt://key/port.sh
    - user: root
    - group: root
    - mode: 755

 
