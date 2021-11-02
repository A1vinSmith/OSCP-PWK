### Tip
Keep adding all findings to the host

### Find name server
```bash
nslookup -query=ANY

inlanefreight.htb       nameserver = ns.inlanefreight.htb.
```

or 

```bash
nslookup -type=NS inlanefreight.htb <IP>
```

### Identify zones exist on the target nameserver
```bash
❯ export TARGET="inlanefreight.htb"                
❯ nslookup -type=any -query=AXFR $TARGET ns.inlanefreight.htb
Server:         ns.inlanefreight.htb
Address:        10.129.42.195#53

inlanefreight.htb
        origin = inlanefreight.htb
        mail addr = root.inlanefreight.htb
        serial = 2
        refresh = 604800
        retry = 86400
        expire = 2419200
        minimum = 604800
inlanefreight.htb       nameserver = ns.inlanefreight.htb.
Name:   dc2.inlanefreight.htb
Address: 10.10.34.11
Name:   internal.inlanefreight.htb # <-- another one
Address: 127.0.0.1
Name:   ns.inlanefreight.htb
Address: 127.0.0.1
```

### Find a TXT record
```bash
❯ nslookup -query=TXT internal.inlanefreight.htb ns.inlanefreight.htb
Server:         ns.inlanefreight.htb
Address:        10.129.30.55#53

internal.inlanefreight.htb    text = "ZONE_TRANSFER{87o2z3cno7zsoiedznxoi82z3o47xzhoi}"
```

### Find some subdomain and FQDN
##### Zone Transfer using Nslookup against the target domain and its nameserver
```bash
nslookup -type=any -query=AXFR inlanefreight.htb ns.inlanefreight.htb
nslookup -type=any -query=AXFR internal.inlanefreight.htb ns.inlanefreight.htb
```

### Find subdomain without nameserver
`subscraper example.com`
