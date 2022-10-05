#!/usr/bin/python

import socket
import sys

if len(sys.argv) < 2:
        print "Usage: smtp-enum.py ip <username.txt>"
        sys.exit(0)

# Create a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Server
connect = s.connect((sys.argv[1],25))

# Receive the banner
banner = s.recv(1024)

print banner

with open(sys.argv[2]) as f:
    lines = f.readlines()
    for line in lines:
        # VRFY a user
        s.send('VRFY ' + line.strip() + '\r\n')
        result = s.recv(1024)
        print result

s.close()