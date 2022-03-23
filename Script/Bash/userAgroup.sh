#!/bin/bash

# Prompt the user for username and group
read -p 'Please enter a username: ' username
read -p 'Now enter a group: ' group

userX=$(sed -n "/^$username/p" /etc/passwd | cut -d":" -f1)
groupX=$(sed -n "/^$group/p" /etc/group | cut -d":" -f1)

if [ $userX ] && [ $groupX ]
then
  b=$(id -nG "$username" | grep -i "$group" | cut -d" " -f1)
  if [ $b ] 
  then
    echo "Membership valid!"
  else
    echo "Membership invalid but available to join."
  fi
elif [ $userX ] || [ $groupX ]
then
  echo "One exists, one does not."
else
  echo "Both are not found"
fi
