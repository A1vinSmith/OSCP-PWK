### Cacls on mount
```bash
smbcacls -N '//10.129.230.198/Department Shares' Users

# mount it
sudo mount -t cifs //10.129.230.198/Department\ Shares /mnt

for i in $(ls); do echo $i; smbcacls -N '//10.129.230.198/Department Shares' $i; done
```