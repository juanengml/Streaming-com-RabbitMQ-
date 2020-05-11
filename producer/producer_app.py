from __future__ import absolute_import, unicode_literals
import datetime

from kombu import Connection
from kombu import Exchange
from kombu import Producer
from kombu import Queue

import sys
import time
import cv2

rabbit_url = 'amqp://guest:guest@192.168.0.12:5672//'
conn = Connection(rabbit_url)
channel = conn.channel()
exchange = Exchange("video-exchange", type="direct", delivery_mode=1)
producer = Producer(exchange=exchange, channel=channel, routing_key="video")
queue = Queue(name="video-queue", exchange=exchange, routing_key="video")
queue.maybe_bind(conn)
queue.declare()

capture = cv2.VideoCapture(0)
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

while True:
    ret, frame = capture.read()
    if ret is True:
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        producer.publish(imgencode.tobytes(), content_type='image/jpeg', content_encoding='binary')
    time.sleep(0.001)

capture.release()
