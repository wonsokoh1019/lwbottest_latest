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

RICH_MENUS = {
                "kr": {
                    "name": "calender_bot_rich_menu_kr",
                    "resource_id": "XAAAUFu0VclmHteAMq0SJrW1/4DJ1j0ajQxbIdtvkK1I5gt63XpKL/XbFwZJEpXI6kVsGFovKEYc5KtUBcBxxsOCwlzBDgmEL9MyTZFiS5Odtp2F"
                },
                "jp":
                {
                    "name": "calender_bot_rich_menu_jp",
                    "resource_id": "XAAAUFu0VclmHteAMq0SJrW1/4ANHaiAB4+RAN3n21hvCtV4Cz25Alb2rQZ2pjPCFQiVno6WfxI8jWhl29n/V1R5XpQXHwtdXIBWihjvFuQLkzz5"
                 },
                "en":
                {
                    "name": "calender_bot_rich_menu_en",
                    "resource_id": "XAAAUFu0VclmHteAMq0SJrW1/4B7AfU4XCm+o5siThmOnD1Kckb7ovd013TiozT/pVuN/2hHaP0uB289Fj7rlEpnXLtQLtnRVX2iEYsb5il9VxMO"
                }
            },

IMAGE_CAROUSEL = {
                    "resource_id":{ "kr":["XAAAUO6yD2IJSJ8t9GRDNwMsZPf0KlLXL9XLawyZeGWQ8Cy/OSLvngOurK22XLHmBCEx/QB0CwWJu4H54Dn6KbI9jSf/ztCml7ll6SMu4UJHAIGU",
                                          "XAAAUO6yD2IJSJ8t9GRDNwMsZPdAMne+KzeWulXEg4otoQ8obL00VeXCBE+xqpmQiPibmprHs8RoPUHQLwItsT1rA5t+qG5TUj1NuPLGJ0tnGFP2",
                                          "XAAAUO6yD2IJSJ8t9GRDNwMsZPdlGbXtZEE+aL8lljIkcSADU6q24X+DclB0lgy/NrDUOtYqV8h/9fAqxTD7iaHImpzZgzIchVcTrKLomzWId0RH"],
                                    "en":["XAAAUO6yD2IJSJ8t9GRDNwMsZPcSarBeL9aPiau0gXtYLU01DqCg1y0/aKJEdvO8gxpoSkjwaJ4nVDIjc6l4t/rpo5GZcl88udOxe9/vM6fpg+6c",
                                        "XAAAUO6yD2IJSJ8t9GRDNwMsZPdhnz47NcSLYIT7Wpm78eF5M6qK62s5/HvT2bKpNQeb5LC28WaCjr5glnaVXrcOfgQGGWLsZVjkA3w2wt1TGyCq",
                                        "XAAAUO6yD2IJSJ8t9GRDNwMsZPe4bEkL2tp/BS+N9fMu/YYnJ7FFU9XGqOnooJtkWB48vfiJFMsOkcmUH10vBLR6c2VQzyhMD2TJEOeeUYD9x1xb"],
                                    "jp":["XAAAUO6yD2IJSJ8t9GRDNwMsZPf/xY2kBLpQPutfM+xwGiBK2h55U4O+FZqzpmEG+SP1OpINl4zp7BtlQmB5qFiYOWOcsqz/GhYqNYjgAT4Y7ChK",
                                          "XAAAUO6yD2IJSJ8t9GRDNwMsZPfAYQuWWgcXaBB3ucjQBKgflBlSKnJaDjTPZNrNimT4bL+5QWMWQyE8va2CF1oh5cQnWFTqCcw0A32rPmht1uCi",
                                          "XAAAUO6yD2IJSJ8t9GRDNwMsZPeGPIGLQEKeCGjrG6fGtNa5AmojOnc9UKRI9o/M7t/F/QXFvhJUKSE5UAKpBhWmNNz93aNekf6J58c/ZQ/tVNm2"]
                                }
                },
API_BO =	{
                "headers": {
                    "content-type": "application/json",
                    "charset": "UTF-8"
                },

                "url": "https://alpha-apis.worksmobile.com/"+API_ID+"/message/sendMessage/v2",
                "upload_url":"http://alpha-storage.worksmobile.com/openapi/message/upload.api",
                "push_url": "https://alpha-apis.worksmobile.com/r/"+API_ID+"/message/v1/bot/"+str(BOT_NO)+"/message/push",
                "rich_menu_url": "https://alpha-apis.worksmobile.com/r/"+API_ID+"/message/v1/bot/"+str(BOT_NO)+"/richmenu",

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
    "cache_dir": "./cache",
}
    

