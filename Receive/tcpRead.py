import socket
import pika

HOST = '192.168.1.8'  
PORT = 1234       

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(20)
i = 0

# connect to rabbit
connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='localhost'))
    pika.ConnectionParameters('192.168.1.6', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = connection.channel()
channel.queue_declare(queue='Pi1')

while True:
    client, addr = s.accept()
    
    try:
        print('Connected by: ')
        print(addr)
        # print(type(addr))
        print(addr[0])
        while True:
            data = client.recv(1024)
            # str_data = data.decode("utf8")
            # if str_data == "quit":
            #     break
            i += 1
            if not data:
                print('No message sent or connect error !')
                break
            print(i)
            print("Message sent: " + data)
            channel.basic_publish(exchange='', routing_key='Pi1', body= data)
    finally:
        client.close()

s.close()