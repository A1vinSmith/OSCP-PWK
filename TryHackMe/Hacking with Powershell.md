### Task 3
1. What is the location of the file "interesting-file.txt"
```
Get-ChildItem -Path C:\ -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match 'interesting-file.txt' }
```
or 
```
Get-ChildItem -Path C:\ -Recurse -ErrorAction SilentlyContinue -Include *interesting-file.txt* -File 
```

2. Specify the contents of this file
```
$searchpath = 'C:\Program Files\interesting-file.txt.txt'
Get-Content -Path $searchpath
```

3. How many cmdlets are installed on the system(only cmdlets, not functions and aliases)?
```
Get-Command | Where-Object -Parameter CommandType -eq Cmdlet | measure
```
or
```
Get-Command -Type Cmdlet | measure
```

4. Get the MD5 hash of interesting-file.txt
```
$readablepath = 'C:\Program Files\readable.txt'
Get-FileHash -Algorithm MD5 -Path $searchpath | Out-File -FilePath $readablepath
```

5. What is the command to get the current working directory?
`Get-Location`

6. Check Path
```
Test-Path -Path C:\Users\Administrator\Documents\Passwords
```

7. What command would you use to make a request to a web server?
`Invoke-WebRequest`

8. Base64 decode the file b64.txt on Windows.
```
certutil -decode "C:\Users\Administrator\Desktop\b64.txt" out.txt
Get-Content out.txt | Out-File -FilePath $readablepath
```

### Task 4
1. How many users are there on the machine?
`Get-LocalUser`

2. Which local user does this SID(S-1–5–21–1394777289–3961777894–1791813945–501) belong to?
```
(Get-Command Get-LocalUser).Parameters

Get-LocalUser -SID "S-1-5-21-1394777289-3961777894-1791813945-501"
```

3. How many users have their password required values set to False?
```
Get-LocalUser | Get-Member
```

get this `PasswordRequired       Property   bool PasswordRequired {get;set;}` then use it
```
Get-LocalUser | Where-Object -Property PasswordRequired -Match false
```

4. How many local groups exist?
`Get-LocalGroup | measure`

5. What command did you use to get the IP address info?
`Get-NetIPAddress`

6. How many ports are listed as listening?
```
Get-NetTCPConnection
Get-NetTCPConnection | Get-Member
GEt-NetTCPConnection | Where-Object -Property State -Match Listen | measure
```

8. How many patches have been applied?
`Get-Hotfix | measure`

9. When was the patch with ID KB4023834 installed?
```
(Get-Command Get-HotFix).Parameters
Get-Hotfix -Id KB4023834
```

10. Find the contents of a backup file.
```
Get-ChildItem -Path C:\ -Recurse -ErrorAction SilentlyContinue -Include *.bak* -File
```

11. Search for all files containing API_KEY
```
Get-ChildItem C:\* -Recurse | Select-String -pattern API_KEY
```

12. What command do you do to list all the running processes?
`Get-Process`

13. What is the path of the scheduled task called new-sched-task?
```
Get-ScheduledTask -TaskName new-sched-task
```
or
`schtasks.exe`

14. Who is the owner of the C:\
```
Get-Acl c:/ | Out-File -FilePath $readablepath
```

### Task 5 Basic Scripting Challenge