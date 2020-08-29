import socket

host = "10.10.40.42"
port = 1337
value = 0

# Example reponse
# HTTP/1.0 200 OK
# Content-Type: text/html; charset=utf-8
# Content-Length: 1033
# Server: Werkzeug/0.14.1 Python/3.5.2
# Date: Sun, 29 Mar 2020 18:07:58 GMT

# add 900 3212

while True:
    try:
        old_port = port
        if port == 9765:
            print("Stop!")
            break
        s = socket.socket()
        s.connect((host,  port))
        req = "GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % host
        s.send(req.encode())
        res = str(s.recv(4096), 'utf-8')
        if len(res) > 147:
            res_lines = res.splitlines()
            last_line = res_lines[-1]
            #item[0] - operation / item[1] - value / item[2] - port
            item = last_line.split()
            port = int(item[2])
            if old_port != port:
                if item[0] == 'add':
                    value += float(item[1])
                elif item[0] == 'minus':
                    value -= float(item[1])
                elif item[0] == 'multiply':
                    value *= float(item[1])
                elif item[0] == 'divide':
                    value /= float(item[1])
                else:
                    print("Unknow operation!")
                    break
            print(last_line)
            s.close()
    except:
        s.close()
        pass
print(value)