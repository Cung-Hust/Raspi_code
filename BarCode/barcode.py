# ls -l /dev/hidraw* - xem danh sach thiet bi hid
# sudo chmod 666 /dev/hidraw0 - cap quyen cho cong usb

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.1.21', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = connection.channel()

channel.queue_declare(queue='barcode')

#doc file tu cong USB
fp = open('/dev/hidraw0', 'rb')

try:
    while True:
        # fp.flush()
        buffer  = fp.read(64)  
        code = buffer.decode()
        # print('Test_01-' + str.encode("ascii", "ignore").decode())
        ad = code.encode("ascii", "ignore").decode()
        message = "test - 01 - " + ad
        channel.basic_publish(exchange='', routing_key='barcode', body=ad)
        print(" [x] Sent: " + message)
except:
    connection.close()