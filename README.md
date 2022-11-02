# OSCP
<img width="1348" alt="image" src="https://user-images.githubusercontent.com/24937594/199577713-5eaaced3-7354-4db0-aeb9-c867cc638b5b.png">

### [GitBook](https://alvinsmith.gitbook.io/progressive-oscp/) for better(but less content) reading experience
### Notes and cheatsheets are in Wiki pages. 
### Repo is mostly filled with writeups and scripts.

# Kali Config via vmware/virtualbox(host on Mac)
## *Kali 2021 version already using zsh by default. You probably won't setup that much. Just do powerlevel10K with mate/Konsole terminal
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

# Kali Config via qemu(host on Mac)
## Better alternative choice https://mac.getutm.app/
1. convert .iso to .qcow2
`qemu-img convert kali.iso kali.qcow2`
2. Resize the QCOW2 image
`qemu-img create -f qcow2 kali.qcow2 50G`
3. Magic (no warnings tested on Jul 2021)
```
qemu-system-x86_64 \
-m 8192 \
-cpu host \
-vga std \
-cdrom ./kali.iso \
-accel hvf \
-drive file=./kali.qcow2

Install:

qemu-system-x86_64 \
-m 8192 \
-cpu host \
-vga std \
-cdrom /Users/AlvinSmith/Images/Kali/kali-linux-2021.2-installer-amd64.iso \
-accel hvf \
-drive file=/Users/AlvinSmith/Images/Kali/kali-linux-2021.2-installer-amd64.qcow2


Run:

qemu-system-x86_64 \
-m 8192 \
-cpu host \
-device bochs-display \
-accel hvf \
-drive file=/Users/AlvinSmith/Images/Kali/kali-linux-2021.2-installer-amd64.qcow2

```

# Common Q&A
### Kali Mirror sync in progress. Can't do apt update/clean
`apt install apt-transport-https` https://www.kali.org/blog/kali-linux-repository-https-support/
### Copy&Paste support(You don't need this if you're on VMware fusion or UTM app)
`https://gist.github.com/plembo/21d4a1579850f7fe84301a90f4fcdf9a`
