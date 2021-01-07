import os, sys, pika, _thread, socket

os.system('sudo chmod 666 /dev/hidraw0')
os.system('sudo chmod 666 /dev/hidraw1')

# ket noi rabbit
rb_connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.1.21', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = rb_connection.channel()

channel.queue_declare(queue='barcode')

HOST = '192.168.1.8'

def filter(input):
    b = ''
    for c in input:        
        if c.isprintable() :
            b = b + str(c)    
    return b

def client_service(PORT, fp, hid):
    #thiet lap ket noi tcp
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    
    try:
        client, addr = s.accept()
        print('Connected by', addr)
        while True:
            data = client.recv(1024)
            tcp_data = data.decode("utf8")
            print("Client: " + tcp_data)
            #-----------------------------------------
            fp.flush()
            code = fp.read(64)    
            barcode_data = hid + filter(code.decode())
            print(barcode_data)
            #-----------------------------------------
            message = tcp_data + barcode_data
            print(message)
            #-----------------------------
            # channel.basic_publish(exchange='', routing_key='barcode', body=message)
    except:
        s.close()

try:
    f0 = open('/dev/hidraw0', 'rb')
    f1 = open('/dev/hidraw1', 'rb')
    _thread.start_new_thread(client_service, (1234, f0, "hid - 01 - "))
    # _thread.start_new_thread(client_service, (9000, f1, "hid - 02 - "))
except:
    print("error")
while 1:
    pass