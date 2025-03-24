#!/usr/bin/python3
import socket
import sys

if len(sys.argv) < 3:
    print("Usage: smtp-enum.py <ip> <username.txt>")
    sys.exit(0)

# Create a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Server
try:
    s.connect((sys.argv[1], 25))
    # Receive the banner
    banner = s.recv(1024).decode("utf-8")
    print(banner)
except Exception as e:
    print(f"Error connecting to the server: {e}")
    sys.exit(1)

# Process username file
try:
    with open(sys.argv[2], "r") as f:
        lines = f.readlines()
        for line in lines:
            # VRFY a user
            s.sendall(f"VRFY {line.strip()}\r\n".encode("utf-8"))
            result = s.recv(1024).decode("utf-8")
            print(result)
    s.close()
except FileNotFoundError:
    print(f"File not found: {sys.argv[2]}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
