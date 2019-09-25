#!/bin/env python
# -*- coding: utf-8 -*-

import io
import logging
import json
from calender.externals.data import *
from calender.constants import API_BO, OPEN_API
import tornado.gen
import requests
LOGGER = logging.getLogger("calender")

def upload_content(file_path):

    headers["consumerKey"] = OPEN_API["consumerKey"]
    headers["Authorization"] = "Bearer " + OPEN_API["token"]
    headers["x-works-apiid"] = OPEN_API["apiId"]

    files = {'file': open(file_path, 'rb')}

    url = API_BO["upload_url"]
    LOGGER.info("upload content . url:%s", url)

    response = requests.post(url, files=files, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return None
    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    return response.headers["x-works-resource-id"]

def make_add_rich_menu_body(rich_menu_name):
    size = make_size(2500, 1686)
    bound1 = make_bound(0, 0, 1250, 1286)

    cn_text1 = i18n_display_text("zh_CN", "上班打卡")
    en_text1 = i18n_display_text("en_US", "Get work records")
    kr_text1 = i18n_display_text("ko_KR", "출근 기록 가져오기")
    display_text1 = [cn_text1, en_text1, kr_text1]
    action1 = make_postback_action("sign_in", "출근 기록 가져오기","sign_in", i18n_display_texts=display_text1)

    bound2 = make_bound(0, 1250, 2500, 1286)
    cn_text2 = i18n_display_text("zh_CN", "下班打卡")
    en_text2 = i18n_display_text("en_US", "Get off-duty records")
    kr_text2 = i18n_display_text("ko_KR", "퇴근 기록 가져오기")
    display_text2 = [cn_text2, en_text2, kr_text2]

    action2 = make_postback_action("sign_out", "퇴근 기록 가져오기", "sign_out", i18n_display_texts = display_text2)

    bound3 = make_bound(0, 1286, 2500, 1686)
    cn_text3 = i18n_display_text("zh_CN", "回到首页")
    en_text3 = i18n_display_text("en_US", "Back to the front page")
    kr_text3 = i18n_display_text("ko_KR", "홈페이지로 돌아오다")
    display_text3 = [cn_text3, en_text3, kr_text3]

    action3 = make_postback_action("to_firt", "홈페이지로 돌아오다","to_firt", i18n_display_texts = display_text3)

    rich_menu = make_add_rich_menu(rich_menu_name,
                   size,
                   [make_area(bound1, action1),make_area(bound2, action2),make_area(bound3, action3)])

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    headers["Authorization"] = "Bearer " + OPEN_API["token"]

    url = API_BO["rich_menu"]["url"]
    LOGGER.info("push message . url:%s", url)

    response = requests.post(url, data=json.dumps(rich_menu), headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return None
    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    tmp = json.loads(response.content)
    return tmp["richMenuId"]

def set_rich_menu_image(resource_id, rich_menu_id):

    body = {"resourceId": resource_id}

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    headers["Authorization"] = "Bearer " + OPEN_API["token"]

    url = API_BO["rich_menu"]["url"] + "/" + rich_menu_id + "content"
    LOGGER.info("push message . url:%s", url)

    response = requests.post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return False
    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    return True

def set_user_specific_rich_menu(rich_menu_id, account_id):
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    headers["Authorization"] = "Bearer " + OPEN_API["token"]
    url = API_BO["rich_menu"]["url"] + "/" + rich_menu_id + "/account/"+ account_id

    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return False,"set user specific rich menu failed."
    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    return True,None

def get_rich_menus():
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    headers["Authorization"] = "Bearer " + OPEN_API["token"]
    url = API_BO["rich_menu"]["url"]

    LOGGER.info("push message begin. url:%s", url)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return None
    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    tmp = json.loads(response.content)
    return tmp["richmenus"]

def canncel_user_specific_rich_menu(account_id):
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    headers["Authorization"] = "Bearer " + OPEN_API["token"]
    url = API_BO["rich_menu"]["url"] + "account/" + account_id

    LOGGER.info("push message begin. url:%s", url)
    response = requests.DELETE(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return False
    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    return True

def init_rich_menu(rich_menu_name):

    rich_menus = get_rich_menus()
    if rich_menus is not None:
        LOGGER.info("body:%s", rich_menus)
        for menu in rich_menus:
            if menu["name"] == rich_menu_name:
                return menu["richMenuId"]
    rich_menu_id = make_add_rich_menu_body(rich_menu_name)
    if not set_rich_menu_image(API_BO["rich_menu"]["resource_id"], rich_menu_id):
        rich_menu_id = None
    return rich_menu_id
