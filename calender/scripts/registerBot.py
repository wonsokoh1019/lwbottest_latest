#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import requests
import json
from common import *
import argparse


admin = ADMIN_ACCOUNT
callback_address = CALLBACK_URL
domain_id = DOMAIN_ID
api_id = API_ID
consumer_key = CONSUMER_KEY
token = TOKEN
headers = {
    "consumerKey": consumer_key,
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "charset": "UTF-8"
}


def create_bot(api_domain, photo_url):
    url = "https://" + api_domain + "/r/" + api_id + "/message/v1/bot"
    data = {
        "name": "근태관리 봇1",
        "i18nNames": [
            {
                "language": "ko_KR",
                "name": "근태관리 봇1"
            },
            {
                "language": "ja_JP",
                "name": "勤怠管理Bot1"
            },
            {
                "language": "en_US",
                "name": "Attendance management bot"
            }
        ],
        "photoUrl": photo_url,
        "i18nPhotoUrls": [
            {
                "language": "ko_KR",
                "photoUrl": photo_url
            },
            {
                "language": "ja_JP",
                "photoUrl": photo_url
            },
            {
                "language": "en_US",
                "photoUrl": photo_url
            }
        ],
        "description": "근태관리 봇",
        "i18nDescriptions": [
            {
                "language": "ko_KR",
                "description": "근태관리 봇"
            },
            {
                "language": "ja_JP",
                "description": "勤怠管理Bot"
            },
            {
                "language": "ja_JP",
                "description": "Attendance management bot"
            }
        ],
        "managers": [admin],
        "submanagers": [],
        "useGroupJoin": False,
        "useDomainScope": False,
        "useCallback": True,
        "callbackUrl": callback_address,
        "callbackEvents": ["text", "location", "sticker", "image"]
    }

    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code != 200:
        print(r.text)
        print(r.content)
        return None
    tmp = r.json()
    print(tmp)
    return tmp["botNo"]


def add_domain(bot_no, api_domain):
    url = "https://" + api_domain + "/r/" + api_id + "/message/v1/bot/" \
          + str(bot_no) + "/domain/" + str(domain_id)
    data = {"usePublic": True, "usePermission": False}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.json())


def main():
    parser = argparse.ArgumentParser(description="Batch Register")
    parser.add_argument('-e', '--env', default='alpha')
    parser.add_argument('-u', '--update', default='none')
    args = parser.parse_args()

    print(args)

    env = args.env
    api_domain = "alpha-apis.worksmobile.com"
    if env == "stage":
        api_domain = "stage-apis.worksmobile.com"
    if env == "real":
        api_domain = "apis.worksmobile.com"

    photo_url = "https://developers.worksmobile.com/favicon.png"
    if PHOTO_URL is not None:
        photo_url = PHOTO_URL

    bot_no = create_bot(api_domain, photo_url)
    add_domain(bot_no, api_domain)

    if args.update == "update":
        root_path = ABSDIR_OF_PARENT + "/calender/constants/"
        with open(root_path + "value.py_template", "r+") as A:
            read_lines = A.readlines()
        write_lines = []
        for line in read_lines:
            if line.find("BOT_NO =") >= 0:
                pos = line.find("=")
                line = line[:pos+1] + " "+str(bot_no) + "\n"
            write_lines.append(line)
        with open(root_path + "value.py", "w") as A:
            A.writelines(write_lines)
    print(bot_no)


if __name__ == "__main__":
    main()
