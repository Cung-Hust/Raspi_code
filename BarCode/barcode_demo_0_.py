# # ls -l /dev/hidraw* - xem danh sach thiet bi hid
# # sudo chmod 666 /dev/hidraw1 - cap quyen cho cong usb

# import pika

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters('192.168.1.21', 5672, '/', pika.PlainCredentials('avani', 'avani')))
# channel = connection.channel()

# channel.queue_declare(queue='barcode')

# # doc file tu cong USB
# fp = open('/dev/hidraw1', 'rb')

# while True:
#     try:
#         fp.flush()
#         buffer  = fp.read(128) 
#         code = buffer.decode()
#         # print('Test_01-' + str.encode("ascii", "ignore").decode())
#         ad = code.encode("ascii", "ignore").decode()
#         message = "test - 02 - " + ad
#         channel.basic_publish(exchange='', routing_key='barcode', body=buffer)
#         print(" [x] Sent: " + buffer)
#     except:
#         connection.close()

# ls -l /dev/hidraw*

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.1.21', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = connection.channel()

channel.queue_declare(queue='barcode')

fp = open('/dev/hidraw1', 'rb')


try:
    while True:
        # fp.flush()
        buffer = fp.read(64)  
        code = buffer.decode()
        message = code.encode("ascii", "ignore").decode()
        print("test - 02 - " + message)
        channel.basic_publish(exchange='', routing_key='barcode', body=message.encode("ascii", "ignore").decode())
        print("message sent !")
except:
    connection.close()