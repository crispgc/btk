import pika
import time
import pandas as pd

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
print(' [*] Reading refseq')
df = pd.read_csv("/Users/cristianperez/full_refseq.bed", header=None, sep='\t')
print(' [*] Refseq loaded')
df.columns = ['chromosome', 'start', 'end', 'gene', 'transcript', 'exon']

def callback(ch, method, properties, body):
    body = body.decode()
    genename = body
    gene_df = df[df['gene'] == genename]
    print(f" [x] Found {len(gene_df)} lines for gene {genename}")
    print(gene_df.head())
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()