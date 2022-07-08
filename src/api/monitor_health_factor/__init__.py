# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask import Blueprint

from .controller import *

rest_monitor_liquidation = Blueprint('rest_monitor_liquidation', __name__, url_prefix='/monitor')

rest_monitor_liquidation.add_url_rule('health_factor/<user_id>',
                                      methods=['GET'],
                                      view_func=get_latest_health_factor_by_user_id)
