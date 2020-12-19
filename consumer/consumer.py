import cv2
import numpy as np
import sys
import time
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from datetime import datetime as dt
import uuid

rabbit_url = 'amqp://guest:guest@3.80.172.11:5672//'


def Model(frame):
    # aqui
    # codigo entra aqui
    #
    print(uuid.uuid1(),type(frame))

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
        Model(image)
        cv2.imshow("image", image)
        cv2.waitKey(1)
        print(dt.now())
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
