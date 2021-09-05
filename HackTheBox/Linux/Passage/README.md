### Bash way
```
for i in $(find . -name "*.php"); do tail -1 $i | base64 -d; echo; done

for i in $(find . -name "*.php"); do tail -1 $i | base64 -d; echo; done | grep -oP [a-z0-9]{64}  # YES
for i in $(find . -name "*.php"); do tail -1 $i | base64 -d; echo; done | grep -oE [a-z0-9]{64}  # YES
for i in $(find . -name "*.php"); do tail -1 $i | base64 -d; echo; done | grep -oG [a-z0-9]{64}  # NO
for i in $(find . -name "*.php"); do tail -1 $i | base64 -d; echo; done | grep -oF [a-z0-9]{64}  # NO
```

### Start with a single quote
```
grep  ^\' .viminfo

'0  12  7  /etc/dbus-1/system.d/com.ubuntu.USBCreator.conf
'1  2  0  /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf
```

###
grep AdminIdentities /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf

### Before pspy
```
ps -ef | grep -i SERVICE
```

### Google USBCreator
https://unit42.paloaltonetworks.com/usbcreator-d-bus-privilege-escalation-in-ubuntu-desktop/


A blog post from Palo Alto’s Unit42 from July 2019 shows a flaw they found in the USBCreator D-Bus interface which:

    Allows an attacker with access to a user in the sudoer group to bypass the password security policy imposed by the sudo program. The vulnerability allows an attacker to overwrite arbitrary files with arbitrary content, as root – without supplying a password. This trivially leads to elevated privileges, for instance, by overwriting the shadow file and setting a password for root.

D-Bus is a messaging system that is a core system on many Linux systems, allowing for communications between processes running on the same system. This vulnerability is in how this process, interface mistakenly allows for an attacker to trigger it to do something unintended, arbitrary write as root.