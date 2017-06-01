import logging
import asyncio
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_0

from time import gmtime, strftime
from datetime import datetime

import re,json

import water_log_store as store

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#topics will contain the sensor id for now something like version/deviceid123/dataLabel -- less verbose is more managable
#so for instance alpha/alpha_deviceid123/temp

TOPIC = 'alpha/+/temp'
BROKER = 'mqtt://beaglebone.local'
MQTT_PORT = '4444'

@asyncio.coroutine
def subscriber_coro():
    C = MQTTClient()

    #mqtt[s]://[username][:password]@host.domain[:port]

    yield from C.connect(BROKER+':'+MQTT_PORT)
    yield from C.subscribe([(TOPIC,QOS_0)])

    print(C.client_id)
    while True:
        try:
            message = yield from C.deliver_message()

            logger.debug(message.__dict__)

            packet = message.publish_packet

            sensor_id = re.split('_|/',packet.variable_header.topic_name)[-2]
            ts = message.publish_packet.protocol_ts
            data = str(packet.payload.data,"utf-8")

            logger.debug("%s => %s => %s" % (packet.variable_header.topic_name, str(packet.payload.data,"utf-8"), strftime("%Y-%m-%d %H:%M:%S", gmtime())))

            message_data = dict([("sensor_id",sensor_id),("temperature",data),("time_stamp",ts.isoformat())])
            data_json = json.dumps(message_data)
            # print(data_json)
            store.handle_microgreens_data(data_json)

        except Error as ce:
            logger.error("trigger disconnet: ", ce)
            break

    yield from C.unsubscribe([(TOPIC,QOS_0)])
    logger.info("UnSubscribed")
    yield from C.disconnect()

if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(subscriber_coro())
