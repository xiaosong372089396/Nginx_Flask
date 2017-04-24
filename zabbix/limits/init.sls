/etc/security/limits.conf:
  file.managed:
    - source: salt://limits/limits.conf
    - user: root
    - group: root
    - mode: 644


