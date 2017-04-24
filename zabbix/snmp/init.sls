net_snmp:
  pkg.installed:
    - pkgs:
      - net-snmp
      - net-snmp-utils

  service:
    - name: snmpd
    - running
    - enable: True
    - reload: True
    - required:
      - pkgs:
        - net-snmp
        - net-snmp-utils
    - reload: True
    - watch:
      - file: /etc/snmp/snmpd.conf

/etc/snmp/snmpd.conf:
  file.managed:
    - source: salt://snmp/snmpd.conf
    - user: root
    - group: root
    - mode: 644
    - backup: minion
