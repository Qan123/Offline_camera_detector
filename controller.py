import pika
import json
import time
from datetime import datetime

# set up connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create queue
channel.queue_declare(queue='camera_events')

def callback(ch, method, properties, body):    
    decoded_string = body.decode("utf-8").replace("b", "").replace("'", "")
    split_string = decoded_string.split()
    print(decoded_string)
    
    timestamp = split_string[1]
    
      
channel.basic_consume(queue='camera_events', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
channel.close()


            

