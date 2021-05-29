# OSCP
### [GitBook](https://alvinsmith.gitbook.io/progressive-oscp/) for better(but less content) reading experience
### Notes and cheatsheets are in Wiki pages. 
### Repo is mostly filled with writeups and scripts.

# Kali Config
### ohmyzsh + powerlevel10K + tmux
tips for Kali 2020.3: Restart the machine after installing oh-my-zsh. It's the most simple way to do it.

### Set root
`sudo dpkg-reconfigure kali-grant-root`

### font
1. Goto `~/.config/qterminal.org` folder
2. Change `fontFamily` to `Fira Code`, `Fira-Code` or something else and save exit.
3. All set, remember don't use Qterminal to do the above steps, otherwise, changes won't take place. Use editor directly open file instead.
4. Should all working now. Either use mate-terminal or do it with GUI editor. 

### .zshrc
1. remove the %(percent sign) when starting a terminal
`unsetopt PROMPT_SP` 

2. make tmux support 256 color
```
if [ "$TERM" != "xterm-256color" ]; then
  export TERM=xterm-256color
fi

alias tmux='TERM=xterm-256color tmux -2'
```

3. you know the drill
`alias apt-get='sudo apt-get'` 
