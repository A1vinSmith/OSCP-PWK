# Setup vulnhub on VMware
![[Setup vulnhub on VMware.png]](https://github.com/A1vinSmith/OSCP-PWK/blob/master/Vulnhub/Setup%20vulnhub%20on%20VMware.png)


### Tips 1
Click "customize setting" before hitting the finish button. Choose "Autodetect" from Bridged Networking. Then `nmap -sT 192.168.1.0/24 -vv` the new available box should pop up. Once you got the idea about how the IP been allocated. 
Run `nmap -sn 192.168.1.0/24`  

or `sudo arp-scan -l` 

or `fping -aqg 192.168.1.0/24` <- This way might be better since not require sudo

for the sake of convenience.

Reinstall if it doesn't work. Try alternatives like VirtualBox if still not working. Cause Some boxes aren’t configured properly so don’t often pick up DHCP. You may find it works properly if you load it on another platform.

### Tips 1
I found out some issues if you put your vuln box under virtualbox and kali in vmware.
1. Patient when your wifi is down. Wait 1min or so.
2. There are might be other ways. But I keep the box under Bridge adapter en0 Wifi. Kali switch between auto-detect and wifi. 
3. It's working eventually. Restart your kali if not.
