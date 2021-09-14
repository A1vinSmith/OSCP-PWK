import base64

#Open file
with open('pw64.txt') as f:
    msg = f.read()

# Decode 13 times
for _ in range(13):
    msg = base64.b64decode(msg)

print(f"The flag is: {msg.decode('utf8')}")

'''
import base64

file = open("b64.txt", "r");
encodedStr = file.read();

i = 0;
while i < 50:
	encodedStr = base64.b64decode(encodedStr);
	i += 1;


print(encodedStr)
'''