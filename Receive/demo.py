import socket
import os
import pika
from thread import *
import time


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
        Connected = pika.BlockingConnection(
            pika.ConnectionParameters('192.168.1.4', 5672, '/', pika.PlainCredentials('avani', 'avani')))
        channel = Connected.channel()
        channel.queue_declare(queue='Pi1')
        channel.basic_publish(exchange='', routing_key='Pi1', body= data)

while True:
    try:
        while True:
            Client, address = ServerSideSocket.accept()
            start_new_thread(multi_threaded_client, (Client, ))
    finally:
        ServerSideSocket.close()