import pika
import os
import time
import logging

def process_request(ch, method, properties, body): 
    print (body)

logging.basicConfig(level=logging.INFO)

# repeatedly try to connect to db and messaging, waiting up to 60s, doubling
# backoff

time.sleep(15)

logging.info("Connecting to messaging service...")

credentials = pika.PlainCredentials(
    os.environ['RABBITMQ_DEFAULT_USER'],
    os.environ['RABBITMQ_DEFAULT_PASS']
)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
            host='messaging',
            credentials=credentials
        )
    )
     
channel = connection.channel()

# create the request queue if it doesn't exist
channel.queue_declare(queue='hello world')

channel.basic_consume(queue='hello world', auto_ack=True,
                      on_message_callback=process_request)

# loops forever consuming from 'request' queue
logging.info("Starting consumption...")
channel.start_consuming()