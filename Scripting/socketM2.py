import socket
import time
import re
import sys

def Main():
    serverIP = sys.argv[1] #Get ip from user input
    serverPort = 1337
    oldNum = 0 #Start at 0 as per instruction

    while serverPort != 9765:
        try: #try until port 1337 available
            if serverPort == 1337:
                print(f"Connecting to {serverIP} waiting for port {serverPort} to become available...")

            #Create socket and connect to server
            s = socket.socket()
            s.connect((serverIP,serverPort))

            #Send get request to server
            gRequest = f"GET / HTTP/1.0\r\nHost: {serverIP}:{serverPort}\r\n\r\n"
            s.send(gRequest.encode('utf8'))

            #Retrieve data from get request
            while True:
                response = s.recv(1024)
                if (len(response) < 1):
                    break
                data = response.decode("utf8")

            #Format and assign the data into usable variables
            op, newNum, nextPort = assignData(data)
            #Perform given calculations
            oldNum = doMath(op, oldNum, newNum)
            #Display output and move on
            print(f"Current number is {oldNum}, moving onto port {nextPort}")
            serverPort = nextPort

            s.close()

        except:
            s.close()
            time.sleep(3) #Ports update every 4 sec
            pass

    print(f"The final answer is {round(oldNum,2)}")

def doMath(op, oldNum, newNum):
    if op == 'add':
        return oldNum + newNum
    elif op == 'minus':
        return oldNum - newNum
    elif op == 'divide':
        return oldNum / newNum
    elif op == 'multiply':
        return oldNum * newNum
    else:
        return None

def assignData(data):
    dataArr = re.split(' |\*|\n', data) #Split data with multi delim
    dataArr = list(filter(None, dataArr)) #Filter null strings
    #Assign the last 3 values of the data
    op = dataArr[-3]
    newNum = float(dataArr[-2])
    nextPort = int(dataArr[-1])

    return op, newNum, nextPort

if __name__ == '__main__':
    Main()

'''
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
		'''
