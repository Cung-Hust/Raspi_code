# ls -l /dev/hidraw* - xem danh sach thiet bi hid
# sudo chmod 666 /dev/hidraw0 - cap quyen cho cong usb

import _thread
import time
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.1.21', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = connection.channel()

channel.queue_declare(queue='barcode')

# fp = open('/dev/hidraw0', 'rb')

def filter(input):
    b = ''
    for c in input:        
        if c.isprintable() :
            b = b + str(c)    
    return b

def scanner(fp, hid):
    while True:
        fp.flush()
        code = fp.read(64)    
        message = hid + filter(code.decode())
        channel.basic_publish(exchange='', routing_key='barcode', body=message)   
        print(message)

try:
    print("Start scan: ...")
    while True:
        f0 = open('/dev/hidraw0', 'rb')
        f1 = open('/dev/hidraw1', 'rb')
        _thread.start_new_thread( scanner, (f0, "" ) )
        _thread.start_new_thread( scanner, (f1, "" ) )
except:
    connection.close()

while 1:
   pass