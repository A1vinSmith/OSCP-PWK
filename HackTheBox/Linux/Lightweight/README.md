### Check with two commands
```bash
ssh 10.10.17.120@10.10.10.119 /usr/sbin/tcpdump -i ens160 -U -s0 -w - not port 22 > ens160no22.pcap

wireshark ens160no22.pcap
```

### It only triggers for visiting status.php which is bad
##### Check in one commands via wireshark live
```bash
ssh 10.10.17.120@10.10.10.119 /usr/sbin/tcpdump -i lo -U -s0 -w - not port 22 | wireshark -k -i -
```

##### Or capture inside the box
```bash
tcpdump -i lo not port 22 -w capture.pcap -v

```

##### If the host only knows the password as sha512, send it what looks like an md5 doesn’t make sense. plain text password
8bc8251332abe1d7f105d3e53ad39ac2