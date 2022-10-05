#!/usr/bin/env python3

import os 
import sys
import re

start = int(sys.argv[2])
end = int(sys.argv[3]) + 1

pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
pattern2 = re.compile(r'64 bytes')

for i in range(start, end):
  address = str(sys.argv[1]) + '.' + str(i)
  response = os.popen(f"ping -c 1 {address}").read()
  res1 = str(pattern.search(response)[0])
  # print(res1)
  if (pattern2.search(response)):
  	print(res1)

# os.popen(f"ip={sys.argv[1]}\n counter={sys.argv[2]}\n end={sys.argv[3]} \nwhile [ $counter -le $end ]\n do ping -c 1 '$ip.$counter' > /dev/null\n [ $? -eq 0 ] && echo '$ip.$counter'\n (($counter++))\n done")