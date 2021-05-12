# List of the values we got using r2 or ghidra
hex_values = ['0x6b', '0x79', '0x6d', '0x7e', '0x68', '0x75', '0x6d', '0x72'] 

username = ""
for char in hex_values:
	username += chr((int(char, 0) - 8) ^ 4)

print(username)


# Alternatie with specify the base explicitly
hex_values2 = ['6b', '79', '6d', '7e', '68', '75', '6d', '72']

username2 = ""
for char in hex_values2:
	username2 += chr((int(char, 16) - 8) ^ 4)

print(username2)