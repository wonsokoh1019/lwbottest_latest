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

API_BO =	{
                "headers": {
                    "content-type": "application/json",
                    "charset": "UTF-8"
                },

                "url": "https://alpha-apis.worksmobile.com/kr1xbFflHaxsx/message/sendMessage/v2",
                "upload_url":"http://alpha-storage.worksmobile.com/openapi/message/upload.api",
                "push_url": "https://alpha-apis.worksmobile.com/r/kr1xbFflHaxsx/message/v1/bot/107796/message/push",

                "rich_menu":
                {
                    "url": "https://alpha-apis.worksmobile.com/r/kr1xbFflHaxsx/message/v1/bot/107796/richmenu",
                    "name": "test_rich_menu",
                    "resource_id":"XAAAUFu0VclmHteAMq0SJrW1/4CKWPq5DOMRCCWpAzUJroxiTpNhtBo86FlPa9IeNwvvkHzfSpBaObDPwoZCdGaqE1zLBaOhLQqdIyWP4ZUvySYK"
                },

                "image_carousel":
                {
                    "resource_id": ["XAAAUO6yD2IJSJ8t9GRDNwMsZPd4hdVveaCll7UqqRDDydLF47nTiwvwHZ/g4YJcCLXP35mhlbOPOOLqI/dcCdqT3c1rRC6dA3Wbyot2++pVKOoJ",
                                    "XAAAUO6yD2IJSJ8t9GRDNwMsZPf77l6CwblhVstm2Ufs3FIjqIbFbg+zZ7ha/P/hF4s0r558lwEA9gV5LOeqKFbtf2CgcsnAIVBmq85qWw0fDmLv",
                                    "XAAAUO6yD2IJSJ8t9GRDNwMsZPc56K5J27l8cxKd1c7ubgQYBowCQe0y3ieE6XsF6AsTy5X0N4h1IygqDqzS/69fBRH0NvYVybILMZsSJfP3cekh"]
                },

                "calendar":
                {
                    "name": "test_calendar",
                    "create_calender_url":"https://alpha-apis.worksmobile.com/kr1xbFflHaxsx/calendar/createCalendar",
                    "get_calenders_url":"https://alpha-apis.worksmobile.com/r/kr1xbFflHaxsx/calendar/rest/v1/users/me/calendarList",
                    "create_schedule_url":"https://alpha-apis.worksmobile.com/kr1xbFflHaxsx/calendar/createSchedule",
                    "modify_schedule_url":"https://alpha-apis.worksmobile.com/kr1xbFflHaxsx/calendar/modifySchedule"
                },

                "TZone":
                {
                    "external_key_url":"https://alpha-apis.worksmobile.com/kr1xbFflHaxsx/calendar/contact/getDomainContact/v1",
                    "time_zone_url":"https://sandbox-apis.worksmobile.com/r/kr1xbFflHaxsx/organization/v2/domains/DOMAIN_ID/users/EXTERNAL_KEY/g11ns"
                }
            }
					
OPEN_API= {
      "_info": "nwetest.com",
      "apiId": "kr1xbFflHaxsx",
      "consumerKey": "2NqRVHLwKJoyhMVweXFI",
      "service_consumerKey": "S_fJOUwLwpew96x7l8es",
      "botNo": 107796,
      "botNames": ["calender bot"],
      "token":"AAAA+UqCOwVLOdscB1a6o7FfTGl+VDzbXCcs35KtxoL+zsB/iqp4Egfa/4LOnh9t8+Omb1ddnTRyNG8J+sYoEYlIBmle9iKzgVQ2vWvczn5a7Wt5aTAc6YnhdJTKt4PjIvDLAueat8VF1CKm4yK1qHpLGp5q47WFqBZqcTJ9Z6u4Xm7GmBo/SeSG6Q9c/6DbqE73M4hxlkdNjjduJEk2Gh8+Fedu0XnY26W9p5+CzzHieE4HdsGFR9uZ16xodc9OoBRSJCkA6bki0E45zfOdkjvE1tAhzYbghgD1vU0nDQwKBM28QhHd70uEbYI6hhYp9I9m3PJzA13ZJ3Xl4q1F1mygfaI="
    }

FILE_SYSTEM = {
    "cache_dir": "/home1/irteam/cache",

}
    

