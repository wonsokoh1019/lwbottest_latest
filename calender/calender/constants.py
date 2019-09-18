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

API_BO =	{
                "method": "POST",
                "headers": {
                    "content-type": "application/json",
                    "charset": "UTF-8"
                },
                "url": "https://alpha-apis.worksmobile.com/API_ID/message/sendMessage/v2"
            }
					
OPEN_API= {
      "_info": "nwetest.com",
      "apiId": "kr1xbFflHaxsx",
      "consumerKey": "2NqRVHLwKJoyhMVweXFI",
      "botNo": 107796,
      "botNames": ["calender bot"],
      "token":"AAAA+UqCOwVLOdscB1a6o7FfTGl+VDzbXCcs35KtxoL+zsB/iqp4Egfa/4LOnh9t8+Omb1ddnTRyNG8J+sYoEYlIBmle9iKzgVQ2vWvczn5a7Wt5aTAc6YnhdJTKt4PjIvDLAueat8VF1CKm4yK1qHpLGp5q47WFqBZqcTJ9Z6u4Xm7GmBo/SeSG6Q9c/6DbqE73M4hxlkdNjjduJEk2Gh8+Fedu0XnY26W9p5+CzzHieE4HdsGFR9uZ16xodc9OoBRSJCkA6bki0E45zfOdkjvE1tAhzYbghgD1vU0nDQwKBM28QhHd70uEbYI6hhYp9I9m3PJzA13ZJ3Xl4q1F1mygfaI="
    }
}
    

