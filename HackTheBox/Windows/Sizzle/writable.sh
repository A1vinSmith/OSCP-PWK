#!/bin/bash
list=$(find /mnt -type d)
for d in $list
do
	touch $d/x 2>/dev/null 
	if [ $? -eq 0 ]
	then
		echo $d " is writable"
	fi
done