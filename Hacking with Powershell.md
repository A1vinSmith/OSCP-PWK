### Task 3
1. What is the location of the file "interesting-file.txt"
```
Get-ChildItem -Recurse | Where-Object { $_.FullName -match 'interesting-file.txt' }
```
2. Specify the contents of this file
```
$searchpath = 'C:\Program Files\interesting-file.txt.txt'
Get-Content -Path $searchpath
```
3.

4. Get the MD5 hash of interesting-file.txt
```
$readablepath = 'C:\Program Files\readable.txt'
Get-FileHash -Algorithm MD5 -Path $searchpath | Out-File -FilePath $readablepath
```