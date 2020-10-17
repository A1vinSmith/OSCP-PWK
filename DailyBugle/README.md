# 1 Joomla version
Use `joomscan` which is pre-installed in kali

# 2 Search the vuln of the specific Joomla version
[Hint](https://github.com/XiphosResearch/exploits) if feel needed: 

# 3 user flag
After getting the Joomla administrator password, we could get a [reverse shell](https://laptrinhx.com/joomla-reverse-shell-503628992/) now. 
Adapt to a [stable shell](https://github.com/A1vinSmith/OSCP-PWK/wiki/Python) with python.

Then `linpeas`, `linEnum` or whatever you prefer.
Suppose to get a hash for the horizontal escalation.
Crack it with hashcat or john. (tips: it's a common password. should only take few seconds to get the result)

`su jjameson` to have the user flag.

# 4 root flag
`sudo -l`
Check the [command](https://gtfobins.github.io/) here

`git clone https://github.com/jordansissel/fpm`

`gem install fpm`

`fpm -n root -s dir -t rpm -a all --before-install root.sh /tmp`

There is also a [blog](https://medium.com/@klockw3rk/privilege-escalation-how-to-build-rpm-payloads-in-kali-linux-3a61ef61e8b2) specifically for privilege escalation this command if needed.
