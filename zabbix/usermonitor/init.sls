usermonitor:
  cmd.run:
    - names: 
      - mkdir -p /var/log/usermonitor 
      - echo usermonitor > /var/log/usermonitor/usermonitor.log 
      - chown nobody:nobody /var/log/usermonitor/usermonitor.log 
      - chmod 002 /var/log/usermonitor/usermonitor.log 
      - chattr +a /var/log/usermonitor/usermonitor.log
      - echo "export HISTORY_FILE=/var/log/usermonitor/usermonitor.log" >> /root/.bash_profile
      - echo "export PROMPT_COMMAND='{ date "+%y-%m-%d %T ##### $(who am i |awk "{print \$1\" \"\$2\" \"\$5}")  #### $(history 1 | { read x cmd; echo "$cmd"; })"; } >>$HISTORY_FILE'" >> /root/.bash_profile
      - echo "export HISTTIMEFORMAT=" $(who am i |awk "{print \$1\" \"\$5}")  |  %F  | %T | "" >> /root/.bash_profile
      - source /root/.bash_profile
       
