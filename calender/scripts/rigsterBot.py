#!/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

admain = "admin@nwetest.com"
callback_address = "https://dev-calenderbot-ncl:2020/callback"
domain_id = 500
api_id = "kr1xbFflHaxsx"
consumer_key = "2NqRVHLwKJoyhMVweXFI"
token = "AAAA9+L83/5eMcw5hk0lA/N5F3gXj6mooeMxdYBT5FKQ9o7Iup4F+hY8vk0PLBBgAufh4qR0MUFxEPzp6dS4dmBG8y3MVqFQhiATJ8bPfJ5eNeymmMyo1I2W51AmI/ninUbXTPaGFcrE/y57MGNXUqrl/9lVaQak5PZVCZz+WhYUGYn5QPk7xWPfjwlwN99H9tlrC/UG2xOKZCbWtwva5+CbUJ1Kdne4afSZRR53V1io28tYl/NUuICIrziJtiRH/pxLnXdzXWre6bTuX/gps4QtplXitWfzzLGBdmxhb5Kum3Q/AHIHbRT5mQ3PsGprVnLBOE/aMoSYUIuUboD6lVUgApU="

headers = {
	"consumerKey": consumer_key,
	"Authorization":"Bearer " + token,
	"Content-Type": "application/json",
	"charset":"UTF-8"
}

def createbot():
	url = "https://alpha-apis.worksmobile.com/r/"+api_id+"/message/v1/bot"
	data = {
		"name": "근태관리 봇",
		"i18nNames": [{
			"language": "ko_KR",
			"name": "근태관리 봇"
		}, 
		{
			"language": "ja_JP",
			"name": "勤怠管理Bot"
		},
		{
			"language": "en_US",
			"name": "Attendance management bot"
		}],
		"photoUrl": "https://developers.worksmobile.com/favicon.png",
		"i18nPhotoUrls": [{
			"language": "ko_KR",
			"photoUrl": "https://developers.worksmobile.com/favicon.png"
		},
		{
			"language": "ja_JP",
			"photoUrl": "https://developers.worksmobile.com/favicon.png"
		},
			{
				"language": "en_US",
				"photoUrl": "https://developers.worksmobile.com/favicon.png"
			}
		],
		"description": "근태관리 봇",
		"i18nDescriptions": [{
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
		}],
		"managers": ["admin@nwetest.com"],
		"submanagers": [],
		"useGroupJoin": False,
		"useDomainScope": False,
		"useCallback": True,
		"callbackUrl": callback_address,
		"callbackEvents": ["text", "location", "sticker", "image"]
	}

	r =requests.post(url, data=json.dumps(data), headers=headers)
	if r.status_code != 200:
		print "create bot failed."
		return None
	tmp = r.json()
	print tmp
	return tmp["botNo"]
def add_domain(bot_no):
	url = "https://alpha-apis.worksmobile.com/r/"+api_id+"/message/v1/bot/"+str(bot_no)+"/domain/"+str(domain_id)
	data = {"usePublic":True,"usePermission":False}
	r =requests.post(url, data=json.dumps(data), headers=headers)
	print r.json()

if __name__ == "__main__":
	bot_no = createbot()
	add_domain(bot_no)
	print bot_no





