#!/usr/bin/env python
import pika
import time

nums = ["100", "200", "300", "400", "500", "600", "700", "800", "900", "1000", "1100", "1200"]
# credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='localhost'))
    pika.ConnectionParameters('192.168.1.5', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = connection.channel()

channel.queue_declare(queue='Pi1')
while True:
    # channel.basic_publish(exchange='', routing_key='hello', body='Hello 1!')
    for num in nums:
        channel.basic_publish(exchange='', routing_key='Pi1', body= num)
        print(" [+] Sent message: " + num)
    print("       -------NEW MESSAGE--------       ")
    time.sleep(1)

connection.close()