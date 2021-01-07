import os
import sys
import socket
import pika
import _thread
import time

# cap quyen cho USB

os.system('sudo chmod 666 /dev/hidraw0')
os.system('sudo chmod 666 /dev/hidraw1')

# khoi tao socket server

ServerSideSocket = socket.socket()
host = '192.168.1.8'
port = 1234

try:
    ServerSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # fix loi tcp using
    ServerSideSocket.bind((host, port))
    # socket.settimeout(5)
except socket.error as e:
    print(str(e))
# print('Socket is listening...')
ServerSideSocket.listen(20)

# ham loc cac ki tu ASCII ma hoa

def filter(input):
    b = ''
    for c in input:        
        if c.isprintable() :
            b = b + str(c)    
    return b


def multi_threaded_client(connection):
    while True:
            data = connection.recv(1024)
            if not data:
                break
            print(data)
            # connect to rabbit
            Connected = pika.BlockingConnection(
                pika.ConnectionParameters('192.168.1.21', 5672, '/', pika.PlainCredentials('avani', 'avani')))
            channel = Connected.channel()
            channel.queue_declare(queue='DEMO - 1')
            channel.basic_publish(exchange='', routing_key='demo', body= data)
            Connected.close()
        # finally:
        #     connection.close()
            # ServerSideSocket.close()

while True:
    try:
        while True:
            Client, address = ServerSideSocket.accept()
            print("Running ...")
            # Client.settimeout(20)
            # print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(multi_threaded_client, (Client, ))
            stop_threads = True
    finally:
        ServerSideSocket.close()
