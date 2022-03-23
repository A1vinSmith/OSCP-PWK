#!/usr/bin/env python3

import re
import gzip
import shutil
from urllib import request

# Define the remote file to retrieve
remote_url = 'http://demo.com/files/access_log.txt.gz'
# Define the local filename to save data
local_file = 'access_log.txt.gz'
# Download remote and save locally
request.urlretrieve(remote_url, local_file)

with gzip.open('access_log.txt.gz', 'rb') as f_in:
    with open('access_log.txt', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

pattern = re.compile(r'[^/]*\.js')
results = set()

with open('access_log.txt') as f:
    for line in f:
        if pattern.search(line) != None: # If a match is found
            results.add(pattern.search(line)[0])

for setItem in results:
    print(setItem)