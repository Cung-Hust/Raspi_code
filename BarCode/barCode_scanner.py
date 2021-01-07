# ls -l /dev/hidraw* - xem danh sach thiet bi hid
# sudo chmod 666 /dev/hidraw0 - cap quyen cho cong usb

import threading
import time
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.1.21', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = connection.channel()

channel.queue_declare(queue='barcode')

fp = open('/dev/hidraw1', 'rb')

def filter(input):
    b = ''
    for c in input:        
        if c.isprintable() :
            b = b + str(c)    
    return b

try:
    print("Start scan ...")
    while True:
        fp.flush()
        code = fp.read(64)    
        message = "S - 01 - " + filter(code.decode())
        channel.basic_publish(exchange='', routing_key='barcode', body=message)   
        print(message)
except:
    connection.close()
