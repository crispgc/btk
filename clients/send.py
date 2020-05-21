import pika
import sys
import random
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

while True:
    message = random.randint(1, 100)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=str(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent %r" % message)
    time.sleep(0.001)

connection.close()