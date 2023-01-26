#!/bin/bash

counter=$2
end=$3

while [ $counter -le $end ]
do
  ping -c 1 "$1.$counter" > /dev/null
  [ $? -eq 0 ] && echo "$1.$counter"
  ((counter++))
done
