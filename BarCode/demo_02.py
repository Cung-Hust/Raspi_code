import socket
import _thread
import pika
import os
import sys
from datetime import datetime

HOST = '192.168.1.8'

os.system('fuser -k 1234/tcp') 
os.system('sudo chmod 666 /dev/hidraw0')
os.system('sudo chmod 666 /dev/hidraw1')

Connected = pika.BlockingConnection(
                pika.ConnectionParameters('192.168.1.21', 5672, '/', pika.PlainCredentials('avani', 'avani'), blocked_connection_timeout=1000,))
channel = Connected.channel()
channel.queue_declare(queue='Pi')

def filter(input):
    b = ''
    for c in input:        
        if c.isprintable() :
            b = b + str(c)    
    return b

def multi_client(PORT, fp, hid):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    os.system('fuser -k 1234/tcp') 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    # s.settimeout(1000)
    s.listen(2)
    try:
        client, addr = s.accept()
        print('Connected by', addr)
        while True:
            s.settimeout()
            data = client.recv(1024)
            tcp_data = data.decode("utf8")
            print("- TCP data: " + tcp_data)

            fp.flush()
            code = fp.read(64)    
            barcode_data = hid + filter(code.decode())
            print("- Bar code: " + barcode_data)

            now = datetime.now()
            time_now = now.strftime("%d/%m/%Y %H:%M:%S")

            message = time_now + " - " + tcp_data + barcode_data

            channel.basic_publish(exchange='', routing_key='Pi', body= message)
            print("- Message sent: " + message)
            print(" ... " * 5)
            # s.close()
    except socket.error as e:
        print("error: ", end="")
        print(str(e))
        # s.close()
try:
    f0 = open('/dev/hidraw0', 'rb')
    f1 = open('/dev/hidraw1', 'rb')
    _thread.start_new_thread(multi_client, (1234, f0, ' - hid - 0 - '))
    _thread.start_new_thread(multi_client, (9000, f1, ' - hid - 1 - '))
except:
    print ("ERROR !!!")
while 1:
   pass