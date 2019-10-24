#!/bin/env python
# -*- coding: utf-8 -*-
import os


# account
LANG = "kr"    # ["kr"|"en"|"jp"]
ADMIN_ACCOUNT = "admin@krbot.com"
RECEIVE_ACCOUNT = "admin02@nwetest.com"
DOMAIN_ID = 18644

# api
API_ID = "kr1EHAIjvfJVz"
CONSUMER_KEY = "To8SnC7sLIAv8GjqXZhO"
TOKEN = "AAAA9iXhCP9TqAVK2ic1mYIEybAyrWVYfg9q/GwxmwkmqneLCYFcR3VhWwfcOuHwh" \
        "UBu7YCTASpWUpqBZqC38TgiraxVgRNv9HgA+Kj17mTE2XCmqxNMyaTLVQ6hrwck4J" \
        "qYqsQ8ldBUd8dEp2i7CqkbPf7sCWuV6HK6VLR6OcmG9xCZMbhL1hnuvvKywWeJun+" \
        "aLfpF4weoF/kF7LvTOicloLBd+XieqNTY+ChsdMYKP3VeeYRwE6mWGON9qWfJ5VqK" \
        "HDEiaF7tdBWKNKM12qtk9yiyZ+CMf8kfVFPnBHVgX0AZjrfiZXAo2qnh0AF/J0MdM" \
        "5EggY9vmmcOpc9/FmHfPFo="

# register bot
CALLBACK_URL = "https://dev-calenderbot-ncl:8080/callback"
PHOTO_URL = None

# root path
ABSDIR_OF_SELF = os.path.dirname(os.path.abspath(__file__))
ABSDIR_OF_PARENT = os.path.dirname(ABSDIR_OF_SELF)
ABSDIR_OF_ROOT = os.path.dirname(ABSDIR_OF_PARENT)
