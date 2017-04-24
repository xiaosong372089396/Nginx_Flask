zabbix-agent:
  pkg.installed:
    - pkgs:
      - zabbix
      - zabbix-agent

  service:
    - name: zabbix-agent
    - running
    - enable: True
    - reload: True
    - required:
      - pkgs:
        - zabbix
        - zabbix-agent
    - reload: True
    - watch:
      - file: /etc/zabbix/zabbix_agentd.conf

/etc/zabbix/zabbix_agentd.conf:
  file.managed:
    - source: salt://zabbix/zabbix_agentd.conf
    - user: root
    - group: root
    - mode: 644
    - backup: mionion
