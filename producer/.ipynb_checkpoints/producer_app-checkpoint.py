from __future__ import absolute_import, unicode_literals
import datetime

from kombu import Connection
from kombu import Exchange
from kombu import Producer
from kombu import Queue

import sys
import time
import cv2

#rabbit_url = 'amqp://guest:guest@172.31.43.223:5672//'
rabbit_url = 'amqp://guest:guest@172.31.43.223:5672//'
print("[*] Conectando no rabbitMQ")

conn = Connection(rabbit_url)
channel = conn.channel()

print("[*] Conectando na exchange pose-estimation")

exchange = Exchange("pose-estimation", type="direct", delivery_mode=1)
producer = Producer(exchange=exchange, channel=channel, routing_key="video")
queue = Queue(name="pose-estimation", exchange=exchange, routing_key="video")

queue.maybe_bind(conn)
queue.declare()

print("[*] Pegando MP4 video ")
capture = cv2.VideoCapture("t014_c02_20200304_18.avi")
print("[*] ENCODING PARAMETER  ")
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

while True:
#    print("SEND FRAME TO CONSUMER ")
    ret, frame = capture.read()
#    print(len(frame))
    if ret is True:
        print("[*] PUBLICANDO DATA IN CONSUMER len(frame): ",len(frame))
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        producer.publish(imgencode.tobytes(), content_type='image/jpeg', content_encoding='binary')
    time.sleep(0.001)

capture.release()
