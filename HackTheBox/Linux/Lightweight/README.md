### Check with two commands
```bash
ssh 10.10.17.120@10.10.10.119 /usr/sbin/tcpdump -i ens160 -U -s0 -w - not port 22 > ens160no22.pcap

wireshark ens160no22.pcap
```

### Check in one commands via wireshark live
```bash
ssh 10.10.17.120@10.10.10.119 /usr/sbin/tcpdump -i lo -U -s0 -w - not port 22 | wireshark -k -i -
```