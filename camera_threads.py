import threading
import random
import time
import pika
import json
from datetime import datetime


def send_to_queue(event):
	# set up connection to RabbitMQ server
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	# create queue
	channel.queue_declare(queue='camera_events')
	    # send event to queue
	channel.basic_publish(exchange='',
		             routing_key='camera_events',
		             #body=json.dumps(event))
		             body=str(event))
	channel.close()
	

def send_offline_cameras(event):
	# set up connection to RabbitMQ server
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	# create queue
	channel.queue_declare(queue='num_cameras_offline')
	    # send event to queue
	channel.basic_publish(exchange='',
		             routing_key='num_cameras_offline',
		             body=str(event))
	channel.close()


class CameraEmulator(threading.Thread):
    def __init__(self, id):
        super(CameraEmulator, self).__init__()
        self.id = id
        self.is_running = True

    def run(self):
        while self.is_running:
            # generate random event data
            timestamp= time.time()
            event_data = f"At, {time.ctime(timestamp)}, thread{self.id}, recieve message of event{random.randint(10000, 11000)}"
            

            print(f"At [{time.ctime(timestamp)}], thread {self.id} is sending messages")
            # send event
            send_to_queue(event_data)
            

            # wait for a random interval between 10 and 110 seconds
            interval = random.randint(10, 110)
            time.sleep(interval)
        


    def stop(self):
        self.is_running = False

class MultiThreadedCameraEmulator:
    def __init__(self, num_cameras):
        self.num_cameras = num_cameras
        self.cameras = []
        self.offline_cameras = set()

    def start(self):
        for i in range(self.num_cameras):
            camera = CameraEmulator(i)
            self.cameras.append(camera)
            camera.start()

        while True:
            num_offline_cameras = random.randint(1, int(0.3*self.num_cameras))
            offline_cameras_list = random.sample(self.cameras, num_offline_cameras)
            # decide how many cameras go offline
            offline_cameras = offline_cameras_list
            #num_cameras_offline(offline_cameras)
            
            send_offline_cameras(offline_cameras_list)
            print("Threads goes offline are",offline_cameras_list)
		
            # set offline duration for each camera
            for camera in offline_cameras:
                offline_duration = random.randint(120, 600)
                self.offline_cameras.add((camera, offline_duration))
                #send offline cameras
                

            # wait for 10 seconds before repeating the process
            time.sleep(50)

            # check if any offline cameras should be brought back online
            for offline_camera in list(self.offline_cameras):
                #send_offline_cameras(camera)
                if offline_duration <= 10:
                    camera.is_running = True
                    self.offline_cameras.remove(offline_camera)
                else:
                    offline_duration -= 10
                    self.offline_cameras.remove(offline_camera)
                    self.offline_cameras.add((camera, offline_duration))

    def stop(self):
        for camera in self.cameras:
            camera.stop()
            camera.join()

if __name__ == '__main__':
    emulator = MultiThreadedCameraEmulator(num_cameras=50)
    emulator.start()


