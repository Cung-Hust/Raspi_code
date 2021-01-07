#!/usr/bin/env python
import pika
import time

messages = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]
# credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='localhost'))
    pika.ConnectionParameters('192.168.1.6', 5672, '/', pika.PlainCredentials('avani', 'avani')))
channel = connection.channel()

channel.queue_declare(queue='Pi2')
while True:
    # channel.basic_publish(exchange='', routing_key='hello', body='Hello 1!')
    for message in messages:
        channel.basic_publish(exchange='', routing_key='Pi2', body= message)
        print(" [+] Sent message: " + message)
    print("       -------NEW MESSAGE--------       ")
    time.sleep(1)

connection.close()