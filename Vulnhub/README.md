# Setup vulnhub on VMware
![[Setup vulnhub on VMware.png]](https://github.com/A1vinSmith/OSCP-PWK/blob/master/Vulnhub/Setup%20vulnhub%20on%20VMware.png)


### Tips
Click "customize setting" before hitting the finish button. Choose "Autodetect" from Bridged Networking. Then `nmap -sT 192.168.1.0/24 -vv` the new available box should pop up. Once you got the idea about how the IP been allocated. Run `nmap -sn 192.168.1.0/24` for the sake of convenience.

Reinstall if it doesn't work. Try alternatives like VirtualBox if still not working. Cause Some boxes aren’t configured properly so don’t often pick up DHCP. You may find it works properly if you load it on another platform.