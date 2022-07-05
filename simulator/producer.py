from ast import Constant
import asyncio
import random
from redis import Redis
from datetime import datetime

DEVICES = [
    '491e059d-73a8-40bb-a5a5-f909492161c2',
    '61c31760-f02a-4a12-96f3-e122ccbc6829',
    'd0750604-0c4d-4292-9bda-d16f01f39997'
]

STREAM_KEY = "simulator_stream"

def redis_connection():
    r = Redis("redis", 6379, retry_on_timeout=True)
    return r
connection = redis_connection()
print("connect_to_redis", connection)

async def create_metrics():
    while True:
        for row in DEVICES:
            rand_metric = random.randint(20, 70)
            data = {
                "device_id": row,
                "metric": rand_metric,  # Just some random data
                "report": str(datetime.now())
            }
            resp = connection.xadd(STREAM_KEY, data)
            print("data send: ", data, " response stream: ", resp)
        await asyncio.sleep(60) #in seconds

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(create_metrics())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()