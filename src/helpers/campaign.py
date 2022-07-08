# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""
import json
import traceback
import requests
from src.config import DefaultConfig
import re
from marshmallow import ValidationError


def log_any(x, *args, **kwargs):
    """
        Log any message to json format.
    """
    msg = {
        'msg': x,
    }

    print()
    if args:
        msg['args'] = json.dumps(args)
    if kwargs:
        msg['kwargs'] = json.dumps(kwargs)
    print(msg)
    return json.dumps(msg)


