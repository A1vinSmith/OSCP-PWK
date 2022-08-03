# Graph
### Personal opionion
https://github.com/A1vinSmith/OSCP-PWK/wiki#holy-war-on-fuzzing-tools

### Install inql which github not working for me
`pipx install inql`

and run it

```
inql -t http://192.168.80.201/graphql
```

### Burp post app/json
```
POST /graphql HTTP/1.1
Host: 192.168.80.201
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close
Content-Type: application/json
Content-Length: 40

{"query":"{ users(searchTerm: \"'\") }"}
```

### Payloadallthethings won this round
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection#sql-injection

### Let's SQL injection then