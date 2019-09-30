#!/bin/env python
# -*- coding: utf-8 -*-

import io
import logging
import json
from calender.externals.data import *
from calender.constants import API_BO, OPEN_API, RICH_MENUS
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

    bound0 = make_bound(0, 0, 1250, 1286)
    jp_text0 = i18n_display_text("ja_JP", "出勤を記録する")
    en_text0 = i18n_display_text("en_US", "Record clock-in")
    kr_text0 = i18n_display_text("ko_KR", "출근 기록하기")
    display_text0 = [jp_text0, en_text0, kr_text0]

    jp_label_text0 = make_i18n_label("ja_JP", "出勤を記録する")
    en_label_text0 = make_i18n_label("en_US", "Record clock-in")
    kr_label_text0 = make_i18n_label("ko_KR", "출근 기록하기")
    display_label0 = [jp_label_text0, en_label_text0, kr_label_text0]

    action0 = make_postback_action("sign_in", display_text = "출근 기록하기", label = "출근 기록하기",
                                   i18n_display_texts = display_text0, i18n_labels = display_label0)

    bound1 = make_bound(0, 1250, 2500, 1286)
    jp_text1 = i18n_display_text("ja_JP", "退勤を記録する")
    en_text1 = i18n_display_text("en_US", "Record clock-out")
    kr_text1 = i18n_display_text("ko_KR", "퇴근 기록하기")
    display_text1 = [jp_text1, en_text1, kr_text1]

    jp_label_text1 = make_i18n_label("ja_JP", "退勤を記録する")
    en_label_text1 = make_i18n_label("en_US", "Record clock-out")
    kr_label_text1 = make_i18n_label("ko_KR", "퇴근 기록하기")
    display_label1 = [jp_label_text1, en_label_text1, kr_label_text1]

    action1 = make_postback_action("sign_out", display_text = "퇴근 기록하기", label = "퇴근 기록하기",
                                   i18n_display_texts = display_text1, i18n_labels = display_label1)

    bound2 = make_bound(0, 1286, 2500, 1686)
    jp_text2 = i18n_display_text("ja_JP", "最初へ")
    en_text2 = i18n_display_text("en_US", "Start over")
    kr_text2 = i18n_display_text("ko_KR", "처음으로")
    display_text2 = [jp_text2, en_text2, kr_text2]

    jp_label_text2 = make_i18n_label("ja_JP", "最初へ")
    en_label_text2 = make_i18n_label("en_US", "Start over")
    kr_label_text2 = make_i18n_label("ko_KR", "처음으로")
    display_label2 = [jp_label_text2, en_label_text2, kr_label_text2]

    action2 = make_postback_action("to_firt", display_text = "처음으로", label = "처음으로", i18n_display_texts = display_text2, i18n_labels = display_label2)

    rich_menu = make_add_rich_menu(rich_menu_name,
                   size,
                   [make_area(bound0, action0),make_area(bound1, action1),make_area(bound2, action2)])

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    headers["Authorization"] = "Bearer " + OPEN_API["token"]

    url = API_BO["rich_menu_url"]
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

    url = API_BO["rich_menu_url"] + "/" + rich_menu_id + "/content"
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
    url = API_BO["rich_menu_url"] + "/" + rich_menu_id + "/account/"+ account_id

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
    url = API_BO["rich_menu_url"]

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
    url = API_BO["rich_menu"]["url"] + "/account/" + account_id

    LOGGER.info("push message begin. url:%s", url)
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return False
    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    return True

def init_rich_menu():
    il8n_rich_menu_id = {}
    rich_menus = get_rich_menus()
    if rich_menus is not None:
        LOGGER.info("body:%s", rich_menus)
        for menu in rich_menus:
            if str(menu["name"]) == RICH_MENUS["kr"]["name"]:
                il8n_rich_menu_id[RICH_MENUS["kr"]["name"]] = menu["richMenuId"]
            elif str(menu["name"]) == RICH_MENUS["jp"]["name"]:
                il8n_rich_menu_id[RICH_MENUS["jp"]["name"]] = menu["richMenuId"]
            elif str(menu["name"]) == RICH_MENUS["en"]["name"]:
                il8n_rich_menu_id[RICH_MENUS["en"]["name"]] = menu["richMenuId"]
    if "kr" not in il8n_rich_menu_id:
        rich_menu_id = make_add_rich_menu_body(RICH_MENUS["kr"]["name"])
        if not set_rich_menu_image(RICH_MENUS["kr"]["resource_id"], rich_menu_id):
            LOGGER.error("set rich menu image failed.")
        il8n_rich_menu_id[RICH_MENUS["kr"]["name"]]=rich_menu_id
    if RICH_MENUS["jp"]["name"] not in il8n_rich_menu_id:
        rich_menu_id = make_add_rich_menu_body(RICH_MENUS["jp"]["name"])
        if not set_rich_menu_image(RICH_MENUS["jp"]["resource_id"], rich_menu_id):
            LOGGER.error("set rich menu image failed.")
        il8n_rich_menu_id[RICH_MENUS["jp"]["name"]] = rich_menu_id
    if RICH_MENUS["en"]["name"] not in il8n_rich_menu_id:
        rich_menu_id = make_add_rich_menu_body(RICH_MENUS["en"]["name"])
        if not set_rich_menu_image(RICH_MENUS["en"]["resource_id"], rich_menu_id):
            LOGGER.error("set rich menu image failed.")
        il8n_rich_menu_id[RICH_MENUS["en"]["name"]] = rich_menu_id
    return il8n_rich_menu_id
