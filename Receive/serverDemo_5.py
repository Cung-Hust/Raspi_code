import socket
import os
from thread import *
import time
import rabbitpy

# TCP connect
ServerSideSocket = socket.socket()
host = '192.168.1.8'
port = 1234

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(20)

# def multi_threaded_client(connection):
#     # RabbitMQ connect

#     with rabbitpy.Connection('amqp://avani:avani@localhost:5672/%2f') as conn:
#         with conn.channel() as channel:
#             queue = rabbitpy.Queue(channel, 'Pi1')
#             queue.declare()
#         try:
#             while True:
#                 data = connection.recv(1024)
#                 if not data:
#                     break
#                 print(data)
#                 rabbitpy.publish(exchange_name="", routing_key='Pi1', body=data)
#         except KeyboardInterrupt:
#             print('Exited consumer')
# with rabbitpy.Connection('amqp://avani:avani@localhost:5672/%2f') as conn:
#     with conn.channel() as channel:
#         queue = rabbitpy.Queue(channel, 'Pi1')
#         queue.declare()
try:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    with rabbitpy.Connection('amqp://avani:avani@192.168.1.4:5672/%2f') as conn:
        with conn.channel() as channel:
            queue = rabbitpy.Queue(channel, 'Pi1')
            queue.declare()
        try:
            while True:        
                data = Client.recv(1024)
                if not data:
                    break
                print(data)
                rabbitpy.publish(exchange_name="", routing_key='Pi1', body=data)
        except KeyboardInterrupt:
            print("---exit")
finally:
    ServerSideSocket.close()