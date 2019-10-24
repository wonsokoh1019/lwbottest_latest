#!/bin/bash python3
# -*- coding: UTF-8 -*-
"""
constants.py Defining the constant used for a project.

"""
import os
from calender.constants.common import *
from calender.constants.value import *
# ---------------------------------------------------------------------
# Constants and global variables
# ---------------------------------------------------------------------

SERVICE_CONSUMER_KEY = None
LOCAL = LANG

RICH_MENUS = {
                "kr": {
                    "name": "calender_bot_rich_menu_kr",
                    "resource_id": RICHMENU_KR_RESOURCE
                },
                "jp":
                {
                    "name": "calender_bot_rich_menu_jp",
                    "resource_id": RICHMENU_JP_RESOURCE
                 },
                "en":
                {
                    "name": "calender_bot_rich_menu_en",
                    "resource_id": RICHMENU_EN_RESOURCE
                }
            }

IMAGE_CAROUSEL = {
                    "resource_id":
                    {
                        "kr": [CAROUSELONE_KR_RESOURCE,
                               CAROUSELTWO_KR_RESOURCE,
                               CAROUSELTHREE_KR_RESOURCE],
                        "en": [CAROUSELONE_EN_RESOURCE,
                               CAROUSELTWO_EN_RESOURCE,
                               CAROUSELTHREE_EN_RESOURCE],
                        "jp": [CAROUSELONE_JP_RESOURCE,
                               CAROUSELTWO_JP_RESOURCE,
                               CAROUSELTHREE_JP_RESOURCE]
                    }
                }
API_BO = {
            "headers": {
                "content-type": "application/json",
                "charset": "UTF-8"
            },

            "url": "https://alpha-apis.worksmobile.com/"
                   + API_ID + "/message/sendMessage/v2",
            "upload_url": "http://alpha-storage.worksmobile.com/"
                          "openapi/message/upload.api",
            "push_url": "https://alpha-apis.worksmobile.com/r/"
                        + API_ID + "/message/v1/bot/"
                        + str(BOT_NO) + "/message/push",
            "rich_menu_url": "https://alpha-apis.worksmobile.com/r/"
                             + API_ID + "/message/v1/bot/"
                             + str(BOT_NO) + "/richmenu",

            "calendar":
            {
                "name": "test_calendar",
                "test_calender_id": "test calender id",
                "create_calender_url": "https://alpha-apis.worksmobile.com/"
                                       + API_ID + "/calendar/createCalendar",
                "get_calenders_url": "https://alpha-apis.worksmobile.com/r/"
                                     + API_ID
                                     + "/calendar/rest/v1/users/me/"
                                       "calendarList",
                "create_schedule_url": "https://alpha-apis.worksmobile.com/"
                                       + API_ID + "/calendar/createSchedule",
                "modify_schedule_url": "https://alpha-apis.worksmobile.com/"
                                       + API_ID + "/calendar/modifySchedule",
                "TZone": "Asia/Seoul"
            },

            "TZone":
            {
                "external_key_url": "https://alpha-apis.worksmobile.com/"
                                    + API_ID
                                    + "/calendar/contact/getDomainContact/v1",
                "time_zone_url": "https://sandbox-apis.worksmobile.com/r/"
                                 + API_ID
                                 + "/organization/v2/domains/"
                                   "DOMAIN_ID/users/EXTERNAL_KEY/g11ns"
            }
        }

OPEN_API = {
        "_info": "nwetest.com",
        "apiId": API_ID,
        "consumerKey": CONSUMER_KEY,
        "service_consumerKey": SERVICE_CONSUMER_KEY,
        "botNo": BOT_NO,
        "token": TOKEN
    }

FILE_SYSTEM = {
    "cache_dir": ABSDIR_OF_ROOT+"/cache",
    "image_dir": ABSDIR_OF_ROOT+"/image",
}
