import socket
import os
# import _thread
import pika
from thread import *
import time
# import rabbitpy

# i = 0

# # connect to rabbit
# connection = pika.BlockingConnection(
#     # pika.ConnectionParameters(host='localhost'))
#     pika.ConnectionParameters('192.168.1.4', 5672, '/', pika.PlainCredentials('avani', 'avani')))
# channel = connection.channel()
# channel.queue_declare(queue='Pi1')

# -----------------------------------
# -----------------------------------

# with rabbitpy.Connection('amqp://avani:avani@localhost:5672/%2f') as conn:
#     with conn.channel() as channel:
#         queue = rabbitpy.Queue(channel, 'Pi1')
#         queue.declare()

ServerSideSocket = socket.socket()
host = '192.168.1.8'
port = 1234
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
    # socket.settimeout(5)
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(20)

def multi_threaded_client(connection):
    # connection.send(str.encode('Server is working:'))
    # try: 
        # Client, address = ServerSideSocket.accept()
    while True:
        data = connection.recv(1024)
        # response = 'Server message: ' + data.decode('utf-8')    #ban tin tra ve cho client
        # response = 'Server message: ' + str(data)
        if not data:
            break
        # connection.sendall(str.encode(response))
        # connection.sendall(response)
        print(data)
        # connect to rabbit
        Connected = pika.BlockingConnection(
            # pika.ConnectionParameters(host='localhost'))
            pika.ConnectionParameters('192.168.1.4', 5672, '/', pika.PlainCredentials('avani', 'avani')))
        channel = Connected.channel()
        channel.queue_declare(queue='Pi1')
        channel.basic_publish(exchange='', routing_key='Pi1', body= data)
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
            # stop_threads = True
            # ThreadCount += 1
            # print('Thread Number: ' + str(ThreadCount))
            # print(data)
    finally:
        ServerSideSocket.close()