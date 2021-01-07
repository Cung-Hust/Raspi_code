#!/usr/bin/env python
import socket
import pika
import time

i = 0
TCP_IP = '192.168.1.8'
# TCP_IP = 'localhost'
TCP_PORT = 1234
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

# connect tcp
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
# s.bind((TCP_IP, TCP_PORT))
# s.listen(1)


# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind((TCP_IP, TCP_PORT))
# become a server socket
serversocket.listen(5)

conn, addr = serversocket.accept()
print("Connection address:", addr)

# connect to rabbit
connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='localhost'))
    pika.ConnectionParameters('192.168.1.6', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = connection.channel()
channel.queue_declare(queue='Pi1')

while True:
    data = conn.recv(BUFFER_SIZE)

    if not data: 
        try:
            # create an INET, STREAMing socket
            # serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # bind the socket to a public host, and a well-known port
            # serversocket.bind((TCP_IP, TCP_PORT))
            # become a server socket
            # serversocket.listen(5)
            print( "no data sent or connect error" )
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('192.168.1.8', 1234))
            s.listen(5)
            conn, addr = s.accept()
            print("Connection address:", addr)
            # data = conn.recv(BUFFER_SIZE)
            # print(data)
            break
        except socket.error:  
            time.sleep( 2 )
        # break
    i += 1
    print(i)
    print("    ")
    print(data) #'received data:  ', 
    # conn.send(data)  # echo  socket reset from peer
    channel.basic_publish(exchange='', routing_key='Pi1', body= data)
    # time.sleep(1)
conn.close()