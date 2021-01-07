#!/usr/bin/env python
import pika, sys, os
import time

def main():
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.5'))
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 15672, '/', pika.PlainCredentials('avani', 'avani')))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)