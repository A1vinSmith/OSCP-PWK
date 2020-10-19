# OSCP
### Notes and cheetsheets are in Wiki pages. Repo is mostly filled with TryHackMe writeups and binaries.

# Kali Config
ohmyzsh + powerlevel10K + tmux

### Set root
`sudo dpkg-reconfigure kali-grant-root`

### font
1. Goto `~/.config/qterminal.org` folder
2. Change fontFamily to Fira Code or somethingelse and save exit.
3. All set, remember don't use Qterminal to do the above steps, otherwise changes wont take place. Use editor directly open file instead.
4. Should all working now. Either use mate-terminal or do it with GUI editor. 

### .zshrc
`unsetopt PROMPT_SP` remove the %(percent sign) when starting a terminal

`alias tmux='TERM=xterm-256color tmux -2'` make tmux support 256 color

`alias apt-get='sudo apt-get'` you know the drill
