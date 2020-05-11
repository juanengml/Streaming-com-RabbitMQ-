import cv2
import numpy as np
import sys
import time
from mtcnn import MTCNN
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from bounding_box import bounding_box as bb


rabbit_url = 'amqp://guest:guest@192.168.0.12:5672//'
detector = MTCNN()

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
        print(size,np_array)
        image = cv2.imdecode(np_array, 1)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(img)
        for face in faces:
            left, top, right, bottom = face['box']
            bb.add(image, left, top, right+left, bottom+top, "face", "aqua")
        cv2.imshow("Stream Broker", image)
        cv2.waitKey(1)
        message.ack()


def run():
    exchange = Exchange("video-exchange", type="direct")
    queues = [Queue("video-queue", exchange, routing_key="video")]
    with Connection(rabbit_url, heartbeat=4) as conn:
            worker = Worker(conn, queues)
            worker.run()

if __name__ == "__main__":
    run()
