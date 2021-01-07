#!/usr/bin/python3

# ls -l /dev/hidraw* - xem danh sach thiet bi hid
# sudo chmod 666 /dev/hidraw0 - cap quyen cho cong usb

import os
import sys
import socket
import pika
import _thread
import time

os.system('sudo chmod 666 /dev/hidraw0')
os.system('sudo chmod 666 /dev/hidraw1')

# ket noi rabbit
rb_connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.1.21', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = rb_connection.channel()

channel.queue_declare(queue='barcode')

# tao socket server
# ServerSideSocket = socket.socket()
# host = '192.168.1.8'
# port = 1234

# ServerSideSocket.listen(3)

# try:
#     ServerSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # fix loi tcp using
#     ServerSideSocket.bind((host, port))
    # socket.settimeout(5)
# except socket.error as e:
#     print(str(e))

# ham loc cac ki tu ASCII ma hoa

def filter(input):
    b = ''
    for c in input:        
        if c.isprintable() :
            b = b + str(c)    
    return b

# Dinh nghia ham chay trong thread

def scanner(fp, hid):
    while True:
        fp.flush()
        code = fp.read(64)    
        message = hid + filter(code.decode())
        channel.basic_publish(exchange='', routing_key='barcode', body=message)
        print(message)

# Khoi tao cac thread tuong ung voi cac may quet
try:
    f0 = open('/dev/hidraw0', 'rb')
    f1 = open('/dev/hidraw1', 'rb')
    _thread.start_new_thread( scanner, (f0, 'S - 01 - ', ) )
    _thread.start_new_thread( scanner, (f1, 'S - 02 - ', ) )
except:
   print ("Error !!!")
   rb_connection.close()
while 1:
   pass