#!/bin/bash python3
# -*- coding: UTF-8 -*-
"""
constants.py Defining the constant used for a project.

"""
import os

# ---------------------------------------------------------------------
# Constants and global variables
# ---------------------------------------------------------------------
ABSDIR_OF_SELF           = os.path.dirname(os.path.abspath(__file__))
LOG_CONF_FILE            = ABSDIR_OF_SELF + '/log.conf'
ABSDIR_OF_PARENT         = os.path.dirname(ABSDIR_OF_SELF)

ADMIN_ACCOUNT = "admin@nwetest.com"
DOMAIN_ID = 500
BOT_NO = 107796
API_ID = "kr1xbFflHaxsx"
CONSUMER_KEY = "2NqRVHLwKJoyhMVweXFI"
SERVICE_CONSUMER_KEY = "S_fJOUwLwpew96x7l8es"
TOKEN = "AAAA9+L83/5eMcw5hk0lA/N5F3gXj6mooeMxdYBT5FKQ9o7Iup4F+hY8vk0PLBBgAufh4qR0MUFxEPzp6dS4dmBG8y3MVqFQhiATJ8bPfJ5eNeymmMyo1I2W51AmI/ninUbXTPaGFcrE/y57MGNXUqrl/9lVaQak5PZVCZz+WhYUGYn5QPk7xWPfjwlwN99H9tlrC/UG2xOKZCbWtwva5+CbUJ1Kdne4afSZRR53V1io28tYl/NUuICIrziJtiRH/pxLnXdzXWre6bTuX/gps4QtplXitWfzzLGBdmxhb5Kum3Q/AHIHbRT5mQ3PsGprVnLBOE/aMoSYUIuUboD6lVUgApU="

API_BO =	{
                "headers": {
                    "content-type": "application/json",
                    "charset": "UTF-8"
                },

                "url": "https://alpha-apis.worksmobile.com/"+API_ID+"/message/sendMessage/v2",
                "upload_url":"http://alpha-storage.worksmobile.com/openapi/message/upload.api",
                "push_url": "https://alpha-apis.worksmobile.com/r/"+API_ID+"/message/v1/bot/"+str(BOT_NO)+"/message/push",

                "rich_menu":
                {
                    "url": "https://alpha-apis.worksmobile.com/r/"+API_ID+"/message/v1/bot/"+str(BOT_NO)+"/richmenu",
                    "name": "calender_bot_rich_menu",
                    "resource_id":"XAAAUFu0VclmHteAMq0SJrW1/4CKWPq5DOMRCCWpAzUJroxiTpNhtBo86FlPa9IeNwvvkHzfSpBaObDPwoZCdGaqE1zLBaOhLQqdIyWP4ZUvySYK"
                },

                "image_carousel":
                {
                    "resource_id":{ "ko_KR":["XAAAUO6yD2IJSJ8t9GRDNwMsZPd4hdVveaCll7UqqRDDydLF47nTiwvwHZ/g4YJcCLXP35mhlbOPOOLqI/dcCdqT3c1rRC6dA3Wbyot2++pVKOoJ",
                                    "XAAAUO6yD2IJSJ8t9GRDNwMsZPf77l6CwblhVstm2Ufs3FIjqIbFbg+zZ7ha/P/hF4s0r558lwEA9gV5LOeqKFbtf2CgcsnAIVBmq85qWw0fDmLv",
                                    "XAAAUO6yD2IJSJ8t9GRDNwMsZPc56K5J27l8cxKd1c7ubgQYBowCQe0y3ieE6XsF6AsTy5X0N4h1IygqDqzS/69fBRH0NvYVybILMZsSJfP3cekh"],
                                    "en_US":["XAAAUO6yD2IJSJ8t9GRDNwMsZPd4hdVveaCll7UqqRDDydLF47nTiwvwHZ/g4YJcCLXP35mhlbOPOOLqI/dcCdqT3c1rRC6dA3Wbyot2++pVKOoJ",
                                    "XAAAUO6yD2IJSJ8t9GRDNwMsZPf77l6CwblhVstm2Ufs3FIjqIbFbg+zZ7ha/P/hF4s0r558lwEA9gV5LOeqKFbtf2CgcsnAIVBmq85qWw0fDmLv",
                                    "XAAAUO6yD2IJSJ8t9GRDNwMsZPc56K5J27l8cxKd1c7ubgQYBowCQe0y3ieE6XsF6AsTy5X0N4h1IygqDqzS/69fBRH0NvYVybILMZsSJfP3cekh"],
                                    "ja_JP":["XAAAUO6yD2IJSJ8t9GRDNwMsZPd4hdVveaCll7UqqRDDydLF47nTiwvwHZ/g4YJcCLXP35mhlbOPOOLqI/dcCdqT3c1rRC6dA3Wbyot2++pVKOoJ",
                                    "XAAAUO6yD2IJSJ8t9GRDNwMsZPf77l6CwblhVstm2Ufs3FIjqIbFbg+zZ7ha/P/hF4s0r558lwEA9gV5LOeqKFbtf2CgcsnAIVBmq85qWw0fDmLv",
                                    "XAAAUO6yD2IJSJ8t9GRDNwMsZPc56K5J27l8cxKd1c7ubgQYBowCQe0y3ieE6XsF6AsTy5X0N4h1IygqDqzS/69fBRH0NvYVybILMZsSJfP3cekh"]
                                }
                },

                "calendar":
                {
                    "name": "test_calendar",
                    "create_calender_url":"https://alpha-apis.worksmobile.com/"+API_ID+"/calendar/createCalendar",
                    "get_calenders_url":"https://alpha-apis.worksmobile.com/r/"+API_ID+"/calendar/rest/v1/users/me/calendarList",
                    "create_schedule_url":"https://alpha-apis.worksmobile.com/"+API_ID+"/calendar/createSchedule",
                    "modify_schedule_url":"https://alpha-apis.worksmobile.com/"+API_ID+"/calendar/modifySchedule"
                },

                "TZone":
                {
                    "external_key_url":"https://alpha-apis.worksmobile.com/"+API_ID+"/calendar/contact/getDomainContact/v1",
                    "time_zone_url":"https://sandbox-apis.worksmobile.com/r/"+API_ID+"/organization/v2/domains/DOMAIN_ID/users/EXTERNAL_KEY/g11ns"
                }
            }
					
OPEN_API= {
      "_info": "nwetest.com",
      "apiId": API_ID,
      "consumerKey": CONSUMER_KEY,
      "service_consumerKey": SERVICE_CONSUMER_KEY,
      "botNo": BOT_NO,
      "token":TOKEN
    }

FILE_SYSTEM = {
    "cache_dir": "/home1/irteam/cache",
}
    

