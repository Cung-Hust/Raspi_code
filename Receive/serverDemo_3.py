import socket
import os
import thread

ServerSideSocket = socket.socket()
host = '192.168.1.8'
port = 1234
ThreadCount = 0

i = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening...')
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        response = 'Server message: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(response))
        print(data)
    connection.close()

while True:
    # Client, address = ServerSideSocket.accept()
    try:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        thread.start_new_thread(multi_threaded_client, (Client, ))
        # ThreadCount += 1
        # print('Thread Number: ' + str(ThreadCount))
        i += 1
        print(str(i))
    finally:
        ServerSideSocket.close()