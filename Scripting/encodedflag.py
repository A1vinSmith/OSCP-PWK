import base64

file = open("encodedflag.txt", "r");
encodedStr = file.read();

encodedStr = base64.b16decode(encodedStr);
encodedStr = base64.b16decode(encodedStr);
encodedStr = base64.b16decode(encodedStr);
encodedStr = base64.b16decode(encodedStr);
encodedStr = base64.b16decode(encodedStr);

encodedStr = base64.b32decode(encodedStr);
encodedStr = base64.b32decode(encodedStr);
encodedStr = base64.b32decode(encodedStr);
encodedStr = base64.b32decode(encodedStr);
encodedStr = base64.b32decode(encodedStr);

encodedStr = base64.b64decode(encodedStr);
encodedStr = base64.b64decode(encodedStr);
encodedStr = base64.b64decode(encodedStr);
encodedStr = base64.b64decode(encodedStr);
encodedStr = base64.b64decode(encodedStr);

print(encodedStr)