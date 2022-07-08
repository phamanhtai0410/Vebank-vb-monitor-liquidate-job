# -*- coding: utf-8 -*-

""""
    Copyright (C) 2022 ESOL LABS - All Rights Reserved.

    You may use, distribute and modify this code under the
    terms of the XYZ license, which unfortunately won't be
    written for another century.

    You should have received a copy of the XYZ license with
    this file. If not, please write to: , or visit :
"""

# File: controller.py
# Created at July 6th, 2022
# Author: taipa

"""
   Description:
        -
        -
"""
from lib.decorators import handle_res
from lib.logger import Logger
from src.services.liquidation import LiquidationService


@handle_res(login=False)
def get_latest_health_factor_by_user_id(user_id, *args, **kwargs):
    return LiquidationService.get_hf_by_user_id(user_id)

