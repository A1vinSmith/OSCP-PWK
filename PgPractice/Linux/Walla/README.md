### CVE-2020-24572
8091 -> Google deep -> RaspAP -> Google default creds -> Login to verify the version -> find exploit

### Root
SUDO file writable
```bash
www-data@walla:/home/walter$ ls -lh
total 8.0K
-rw------- 1 www-data walter    33 Oct 18 22:36 local.txt
-rw-r--r-- 1 www-data www-data 208 Oct 18 23:06 wifi_reset.py
```