import cv2
import sys
import time
import uuid
import numpy as np
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from datetime import datetime as dt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import json

with open("config.json") as json_file:
   data = json.load(json_file)


rabbit_url = data['RABBITMQ'] # "amqp://guest:guest@172.31.65.120:5672//"

def Model(frame):
    print(type(frame),dt.now())
    bbox, label, conf = cv.detect_common_objects(frame, confidence=0.2, model="yolov4-tiny")
    print(bbox, label, conf)
    output_image = draw_bbox(frame, bbox, label, conf) 
    return output_image

class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message],
                         accept=['image/jpeg'])]

    def on_message(self, body, message):
        size = sys.getsizeof(body)
        np_array = np.frombuffer(body, dtype=np.uint8)
        image = cv2.imdecode(np_array, 1)
        output_image = Model(image)
#        cv2.imshow("image", output_image)
#        cv2.waitKey(1)
        message.ack()

def run():
    print("[*] CONSUMER APP rabbitMQ ")
    exchange = Exchange("video-exchange", type="direct")
    print("[*] QUEUE: video-queue")
    queues = [Queue("video-queue", exchange, routing_key="video")]
    print("[*] WORKER RUNNING  ")
    with Connection(rabbit_url, heartbeat=40) as conn:
            worker = Worker(conn, queues)
            print("[*] WORKER RUN RABBIT LOADING...")
            worker.run()

if __name__ == "__main__":
    run()
