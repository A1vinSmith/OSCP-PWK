import socket

host = input("Host: ")
port = int(input("Port: "))
req = "GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % host

while True:
	try:
		old_port = port

		if port == 9765:
			print("Stop!")
			break

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port));
		s.send(req.encode())

		result = s.recv(4096)
		res = str(result, 'utf-8')
		res_lines = res.splitlines()
		last_line = res_lines[-1]
		item = last_line.split()
		port = int(item[2])

		print(last_line);

		s.close();
	except:
		s.close();
		pass