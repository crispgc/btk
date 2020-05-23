import pika
import sys
import random
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
genes = ['BRCA1', 'BRCA2', 'KRAS', 'ATRX', 'NRAS', 'KRAS', 'ABRAXAS1', 'SRY']

while True:
    index = random.randint(0, len(genes) - 1)
    print(index)
    message = genes[index]
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=str(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent %r" % message)
    time.sleep(0.2)

connection.close()