import rabbitpy
import time

with rabbitpy.Connection('amqp://avani:avani@192.168.1.4:5672/ad') as conn:
    with conn.channel() as channel:
        queue = rabbitpy.Queue(channel, 'Pi')
        queue.declare()
        # Exit on CTRL-C
        # try:
        #     # Consume the message
        #     # for message in queue:
        #     #     message.pprint(True)
        #     #     message.ack()
        #     rabbitpy.publish(
        #         exchange_name="my_exchange",
        #         routing_key='example',
        #         body='This is my test message')
        # except KeyboardInterrupt:
        #     print('Exited consumer')
try:
    while True:
        data = "Client - 1 - 0000 - 1111"
        rabbitpy.publish(
            exchange_name="example",
            routing_key='Pi',
            body=data)
        print(data)
        time.sleep(0.8)
except KeyboardInterrupt:
    print('Exited consumer')