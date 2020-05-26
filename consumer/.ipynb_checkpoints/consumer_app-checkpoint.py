import cv2
import numpy as np
import sys
import time
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

rabbit_url = 'amqp://guest:guest@172.31.43.223:5672//'

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
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print("[*] CONSUMER RECEBENDO len(frame) RECEBIDO: ",len(img))
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
