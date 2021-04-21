nmap -p-15000 -vv $ip -oG initial-scan
nmap -p 22,80,443,10000 -sV -vv $ip -oG service-scan