# -*- coding: utf-8 -*-

""""
    Copyright (C) 2022 ESOL LABS - All Rights Reserved.

    You may use, distribute and modify this code under the
    terms of the XYZ license, which unfortunately won't be
    written for another century.

    You should have received a copy of the XYZ license with
    this file. If not, please write to: , or visit :
"""

# File: consumer_health_factor_checking.py
# Created at May 17th, 2022
# Author: taipa
from src.models.users import UsersModel


class LiquidationService(object):
    @classmethod
    def get_hf_by_user_id(cls, _user_id):
        _user = UsersModel.db().get_item(oid=_user_id)
        return _user or {}


