#!/bin/env python
# -*- coding: utf-8 -*-
"""
get a user info by account id.
"""

__all__ = ['get_user_info_by_account', 'load_external_key']

from calendar_bot.common.global_data import get_value, set_value
from datetime import datetime, timedelta, timezone
from calendar_bot.common.utils import auth_get, auth_post
from calendar_bot.constant import API_BO, OPEN_API
from conf.config import ADMIN_ACCOUNT
import logging
import pytz
import json

LOGGER = logging.getLogger("calendar_bot")

def get_user_info_by_account(account_id):
    """
    Get user info of account.
    reference: https://developers.worksmobile.com/jp/document/1006004/v1?lang=en
    If you fail to get external key,
    log in to the development console to check your configuration.
    reference: https://auth.worksmobile.com/login/login?
    accessUrl=https%3A%2F%2Fdevelopers.worksmobile.com
    %3A443%2Fconsole%2Fopenapi%2Fmain)

    :return: external key
    """
    contacts_url = "%s?account=%s" % \
                       (API_BO["TZone"]["contacts_url"], account_id)
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "charset": "UTF-8",
        "consumerKey": OPEN_API["consumerKey"]
    }

    response = auth_post(contacts_url, headers=headers)
    if response.status_code != 200 or response.content is None:
        LOGGER.error("get user info failed. url:%s text:%s body:%s",
                    contacts_url, response.text, response.content)
        raise Exception("get user info. http return code error.")
    tmp_req = json.loads(response.content)
    data = tmp_req.get("data", None)
    if data is None:
        raise Exception("get user info. data filed is None.")
    external_key = data.get("externalKey", None)
    name = data.get("name", None)
    if external_key is None:
        raise Exception("get user info. external_key filed is None.")
    return external_key, name


def get_external_key():
    external_key = get_value("externalKey", None)
    return external_key


def set_external_key():
    external_key, _ = get_user_info_by_account(ADMIN_ACCOUNT)
    set_value("externalKey", external_key)

    return external_key


def load_external_key():
    """
    load external key.

    :return: admin account's external key
    """
    external_key = get_external_key()
    if external_key is None:
        external_key = set_external_key()
    return external_key
