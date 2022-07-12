#!/usr/bin/python

import json
import time
import random
import os
import sys
import getopt

sys.path.append(".")

from lib.utils import amqp
from pydash import get
from lib.logger import LoggerTask
from src.config import DefaultConfig
from lib.util import dt_utcnow
from src.models.users import UsersModel
from bson import ObjectId
from src.helpers.vechain import get_health_factor
from src.task import worker


def on_message_health_factor(channel, method, properties, body):
    try:
        msg = body.decode("utf8")
        msg = json.loads(msg)
        _data_msg = msg
        # Log received message
        LoggerTask.debug(_data_msg)
        # parse message
        _user_public_address = get(_data_msg, "address").lower()
        _user_id = get(_data_msg, 'user')
        _args = get(_data_msg, "returnValues")
        _old_hf = get(_data_msg, 'old_hf')
        _new_hf = get_health_factor(_user_public_address)

        print('New HF = ', _new_hf)

        _tx = UsersModel.db().find_one_and_update(
            filter={
                "_id": ObjectId(_user_id)
            },
            update=[{
                "$set": {
                    "hf": _new_hf,
                    "updated_time": dt_utcnow(),
                    "created_time": {"$cond": [{"$not": ["$created_time"]}, dt_utcnow(), "$created_time"]},
                }
            }],
            upsert=True
        )
        if not _tx:
            return f"Reject tx {_tx}"
        channel.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(e)
        channel.basic_nack(delivery_tag=method.delivery_tag)


def handle_msg(_cfg):
    cfg_rabbit = {
        "hostname": DefaultConfig.RABBIT_HOST, "port": DefaultConfig.RABBIT_PORT,
        "username": DefaultConfig.RABBIT_USER, "password": DefaultConfig.RABBIT_PASSWORD,
        "vhost": DefaultConfig.RABBIT_VHOST, "exchange_type": "topic"
    }
    cfg_rabbit.update(_cfg)
    event_name = cfg_rabbit["queue"].split("-")[-1]
    print("cfg_rabbit: ", cfg_rabbit)
    mq = amqp.AmqpConnection(**cfg_rabbit)
    mq.connect()
    mq.setup_queues(durable=True)

    if event_name == "liquidation_health_factor":
        mq.consume(on_message_health_factor)
    else:
        print("Event not found")
        sys.exit(2)


if __name__ == "__main__":
    _cfg = {}
    _exchange = ""
    _routing_key = ""
    _queue = ""
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "k:e:q:", ["routing_key=", "exchange=", "queue="])
    except getopt.GetoptError:
        print("python3 workers/consumer_health_factor_checking.py -e <exchange> -k <routing_key> -q <queue>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("python3 workers/consumer_health_factor_checking.py -e <exchange> -k <routing_key> -q <queue>")
            sys.exit()
        elif opt in ("-e", "--exchange"):
            _exchange = arg
        elif opt in ("-k", "--routing_key"):
            _routing_key = arg
            print("_routing_key: ", _routing_key)
        elif opt in ("-q", "--queue"):
            _queue = arg

    _cfg["exchange"] = _exchange
    _cfg["routing_key"] = _routing_key
    _cfg["queue"] = _queue
    handle_msg(_cfg)
