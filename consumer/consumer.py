from ast import Constant
import asyncio
import random
from redis import Redis
from datetime import datetime
import requests

DEVICES = [
    '491e059d-73a8-40bb-a5a5-f909492161c2',
    '61c31760-f02a-4a12-96f3-e122ccbc6829',
    'd0750604-0c4d-4292-9bda-d16f01f39997'
]

STREAM_KEY = "simulator_stream"

def redis_connection():
    r = Redis("redis", 6379, retry_on_timeout=True)
    return r


def get_data(redis_connection):
    last_id = 0
    sleep_ms = 5000
    while True:
        try:
            resp = redis_connection.xread(
                {STREAM_KEY: last_id}, count=1, block=sleep_ms
            )
            if resp:
                key, messages = resp[0]
                last_id, data = messages[0]
                print("ID: ", messages)
                device = data[b'device_id'].decode('utf-8')
                metric = data[b'metric'].decode('utf-8')
                report = data[b'report'].decode('utf-8')
                
                data_send = {
                    "device_id": device,
                    "metric": metric,
                    "report": report
                }

                #to_del = connection.xdel(STREAM_KEY, last_id.decode('utf-8'))
                connection.xdel(STREAM_KEY, last_id.decode('utf-8'))

                request = requests.post('http://backend:8000/metrics/', data=data_send)
                print("request status: ", request.text, request.status_code)
                #print("to_del", to_del)

                # Check list of events
                #XREAD COUNT 100 STREAMS simulator_stream 0

        except ConnectionError as e:
            print("ERROR REDIS CONNECTION: {}".format(e))


if __name__ == "__main__":
    connection = redis_connection()
    print("connect_to_redis", connection)
    get_data(connection)


