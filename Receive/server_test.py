import socket
import os
import pika
from thread import *
import time

# create socket server
ServerSideSocket = socket.socket()
host = '192.168.1.8'
port = 1234
# ThreadCount = 0

try:
    ServerSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # fix loi tcp using
    ServerSideSocket.bind((host, port))
    # socket.settimeout(5)
except socket.error as e:
    print(str(e))
    # if e.errorno == 98:        

print('Socket is listening...')
ServerSideSocket.listen(20)

def multi_threaded_client(connection):
    while True:
            data = connection.recv(1024)
            if not data:
                # Connected.close()
                break
            print(data)
            # connect to rabbit
            Connected = pika.BlockingConnection(
                pika.ConnectionParameters('192.168.1.21', 5672, '/', pika.PlainCredentials('avani', 'avani')))
            channel = Connected.channel()
            channel.queue_declare(queue='Pi')
            channel.basic_publish(exchange='', routing_key='Pi', body= data)
            Connected.close()
            # time.sleep(1)
        # finally:
        #     connection.close()
            # ServerSideSocket.close()

while True:
    try:
        # Client, address = ServerSideSocket.accept()
        while True:
            Client, address = ServerSideSocket.accept()
            # Client.settimeout(20)
            # print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(multi_threaded_client, (Client, ))
            stop_threads = True
            # ThreadCount += 1
            # print('Thread Number: ' + str(ThreadCount))
    finally:
        ServerSideSocket.close()