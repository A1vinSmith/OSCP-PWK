dnsrecon -r 127.0.0.0/24 -n 10.129.29.200

### DNS zone transfer when 53 opening TCP
https://book.hacktricks.xyz/pentesting/pentesting-dns#zone-transfer

```
# Default root zone
dig axfr @10.129.29.200
# Specific a zone bank.htb
dig axfr bank.htb @10.129.29.200
```

```
bank.htb.               604800  IN      SOA     bank.htb. chris.bank.htb. 6 604800 86400 2419200 604800
bank.htb.               604800  IN      NS      ns.bank.htb.
bank.htb.               604800  IN      A       10.129.29.200
ns.bank.htb.            604800  IN      A       10.129.29.200
www.bank.htb.           604800  IN      CNAME   bank.htb.
bank.htb.               604800  IN      SOA     bank.htb. chris.bank.htb. 6 604800 86400 2419200 604800
```
### Alternative options then /etc/hosts
`/etc/resolv.conf`