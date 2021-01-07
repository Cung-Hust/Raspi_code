import socket
import os
# import _thread
import pika
import thread

i = 0

# connect to rabbit
connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='localhost'))
    pika.ConnectionParameters('192.168.1.6', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = connection.channel()
channel.queue_declare(queue='Pi1')

# -----------------------------------
# -----------------------------------

ServerSideSocket = socket.socket()
host = '192.168.1.8'
port = 1234
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(3)

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(1024)
        # response = 'Server message: ' + data.decode('utf-8')
        response = 'Server message: ' + str(data)
        if not data:
            break
        # connection.sendall(str.encode(response))
        connection.sendall(response)
        print(data)
        channel.basic_publish(exchange='', routing_key='Pi1', body= data)
    # connection.close()

while True:
    try:
        while True:
            Client, address = ServerSideSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            thread.start_new_thread(multi_threaded_client, (Client, ))
            # ThreadCount += 1
            # print('Thread Number: ' + str(ThreadCount))
            # print(data)
    finally:
        ServerSideSocket.close()