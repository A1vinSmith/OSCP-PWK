# 1 Joomla version
Use `joomscan` which is pre-installed in kali

# 2 Search the vuln of the specific Joomla version
Hint if feel needed: https://github.com/XiphosResearch/exploits

# 3 user flag
After the Joomla administrator password, we could get a [reverse shell]: https://laptrinhx.com/joomla-reverse-shell-503628992/ now. 
Use python to get [stable shell]: https://github.com/A1vinSmith/OSCP-PWK/wiki/Python

Then `linpeas`, `linEnum` or whatever you prefer.
Suppose to get a hash for the horizontal escalation.
Crack it with hashcat or john. (tips: it's a common password. should only take few seconds to get the result)

`su jjameson` have the user flag now.

# 4 root flag
`sudo -l`
Check the command in here https://gtfobins.github.io/
`git clone https://github.com/jordansissel/fpm`
`gem install fpm`
`fpm -n root -s dir -t rpm -a all --before-install root.sh /tmp`

There is also a blog specifically for privilege escalation this command if needed.
https://medium.com/@klockw3rk/privilege-escalation-how-to-build-rpm-payloads-in-kali-linux-3a61ef61e8b2