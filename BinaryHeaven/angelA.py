# List of the values we got using r2 or ghidra
hex_values = ['0x6b', '0x79', '0x6d', '0x7e', '0x68', '0x75', '0x6d', '0x72'] 

username = ""
for char in hex_values:
	username += chr((int(char, 0) - 8) ^ 4)

print(username)
