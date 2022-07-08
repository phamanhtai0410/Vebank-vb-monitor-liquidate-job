import time
import sys
import getopt
from bson import json_util
sys.path.append(".")
from lib.utils import amqp
from src.config import DefaultConfig
from src.models.users import UsersModel
from src.constants import AppConstants
from src.task import worker


def main(_cfg):
    cfg_rabbit = {
        "hostname": DefaultConfig.RABBIT_HOST, "port": DefaultConfig.RABBIT_PORT,
        "username": DefaultConfig.RABBIT_USER, "password": DefaultConfig.RABBIT_PASSWORD,
        "vhost": DefaultConfig.RABBIT_VHOST, "exchange_type": "topic"
    }
    cfg_rabbit.update(_cfg)
    # event_name = cfg_rabbit["queue"].split("-")[-1]
    print("cfg_rabbit: ", cfg_rabbit)
    mq = amqp.AmqpConnection(**cfg_rabbit)
    mq.connect()

    _repeated_times = 0
    while True:
        _is_empty = False
        page = AppConstants.DEFAULT_PAGE
        page_size = AppConstants.DEFAULT_PAGE_SIZE
        while not _is_empty:
            print(f"-- * __ Query for user in page {page}, page_size {page_size} !  -- * --")
            _users = list(UsersModel.get_list(
                page=page,
                page_size=page_size
            ))
            page += 1

            if len(_users) == 0:
                _is_empty = True
                continue

            print('users = ', len(_users))

            for _user in list(_users):
                print('hf = ', _user)
                if 'hf' not in _user or _user['hf'] == 0:
                    mq.publish(
                        payload={
                            "type": AppConstants.LAYER_1_JOB_TYPE,
                            "old_hf": _user["hf"] if 'hf' in _user else 0,
                            "user": str(_user["_id"]),
                            "address": _user['address']
                        }
                    )
                    print(f"-- * __ Publish mess __ * -- with payload : {str(_user['_id'])} : {_user['address']}")
                    continue

                if _user['hf'] > AppConstants.HF_LAYER_1:
                    if _repeated_times // AppConstants.REPEATED_LAYER_1 == 0:
                        mq.publish(
                            payload={
                                "type": AppConstants.LAYER_1_JOB_TYPE,
                                "old_hf": _user["hf"],
                                "user": str(_user["_id"]),
                                "address": _user['address']
                            }
                        )
                        print(f"-- * __ Publish mess __ * -- with payload : {str(_user['_id'])} : {_user['address']}")
                    else:
                        continue

                if AppConstants.HF_LAYER_2 <= _user['hf'] < AppConstants.HF_LAYER_1:
                    if _repeated_times // AppConstants.REPEATED_LAYER_2 == 0:
                        mq.publish(
                            payload={
                                "type": AppConstants.LAYER_2_JOB_TYPE,
                                "old_hf": _user["hf"],
                                "user": str(_user["_id"]),
                                "address": _user['address']
                            }
                        )
                        print(f"-- * __ Publish mess __ * -- with payload : {str(_user['_id'])} : {_user['address']}")
                    else:
                        continue

                if AppConstants.HF_LAYER_3 <= _user['hf'] < AppConstants.HF_LAYER_2:
                    if _repeated_times // AppConstants.REPEATED_LAYER_3 == 0:
                        mq.publish(
                            payload={
                                "type": AppConstants.LAYER_3_JOB_TYPE,
                                "old_hf": _user["hf"],
                                "user": str(_user["_id"]),
                                "address": _user['address']
                            }
                        )
                        print(f"-- * __ Publish mess __ * -- with payload : {str(_user['_id'])} : {_user['address']}")
                    else:
                        continue

        _repeated_times += 1
        print("------   * Repeated Times = ", _repeated_times)
        time.sleep(DefaultConfig.SCHEDULED_INTERVAL)


if __name__ == "__main__":
    _cfg = {}
    _exchange = ""
    _routing_key = ""
    _queue = ""
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "k:e:q:", ["routing_key=", "exchange=", "queue="])
    except getopt.GetoptError:
        print("python3 src/schedule_jobs/health_factor_scanner.py -e <exchange> -k <routing_key> -q <queue>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("python3 src/schedule_jobs/health_factor_scanner.py -e <exchange> -k <routing_key> -q <queue>")
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
    print("*** Config command : ", _cfg)
    main(_cfg)
