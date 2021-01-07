import socket
import os
# import _thread
import pika
from thread import *
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.1.5', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = connection.channel()
channel.queue_declare(queue='Pi1')

ServerSideSocket = socket.socket()
host = '192.168.1.8'
port = 1234
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(20)

def multi_threaded_client(connection):
    while True:
        data = connection.recv(1024)
        if not data:
            break
        print(data)
        channel.basic_publish(exchange='', routing_key='Pi1', body= data)
        time.sleep(1)
    # finally:
    #     connection.close()
        # ServerSideSocket.close()

while True:
    try:
        while True:
            Client, address = ServerSideSocket.accept()
            # Client.settimeout(20)
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(multi_threaded_client, (Client, ))
    finally:
        ServerSideSocket.close()