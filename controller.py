import pika
import json
import time
from datetime import datetime

# set up connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create queue
channel.queue_declare(queue='camera_events')

# get total number of cameras
#channel.queue_declare(queue='num_cameras_offline')

#method, properties, body = channel.basic_get(queue='num_cameras_offline')
#num_cameras = int(body.decode('utf-8')) if body else 0

def callback(ch, method, properties, body):    
    decoded_string = body.decode("utf-8").replace("b", "").replace("'", "")
    split_string = decoded_string.split()
    print(decoded_string)
    
    timestamp = split_string[1]
    
      
channel.basic_consume(queue='camera_events', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
channel.close()


            

