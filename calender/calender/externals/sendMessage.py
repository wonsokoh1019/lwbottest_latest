#!/bin/env python
# -*- coding: utf-8 -*-
import io
import logging
import socket
from calender.externals.data import *
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
import requests
from calender.constants import API_BO, OPEN_API

LOGGER = logging.getLogger("calender")

"""
type req struct {
	TenantId string
	BotNo     int64       `json:"botNo"`
	AccountId *string     `json:"accountId,omitempty"`
	RoomId    *string     `json:"roomId,omitempty"`
	Content   interface{} `json:"content"`
}
"""
@tornado.gen.coroutine
def send_message(req, headers): 
	LOGGER.info("deail send_message")
	error_code = False
	headers["consumerKey"] = OPEN_API["consumerKey"]
	headers["Authorization"] = "Bearer " + OPEN_API["token"]

	url = API_BO["url"]
	#url = API_BO["push_url"]
	client = AsyncHTTPClient()
	LOGGER.info("send message . url:%s body:%s headers:%s", url, str(req), str(headers))
	response = yield client.fetch(url, headers=headers, method='POST', body=json.dumps(req))
	if response.code != 200:
		error_code = True
		LOGGER.info("send message failed. url:%s body:%s", url, response.body)
	LOGGER.info("send message success. url:%s body:%s", url,response.body)
	return error_code

@tornado.gen.coroutine
def push_message(req, headers): 
	LOGGER.info("deail push_message")
	error_code = False
	headers["consumerKey"] = OPEN_API["consumerKey"]
	headers["Authorization"] = "Bearer " + OPEN_API["token"]

	url = API_BO["push_url"]
	LOGGER.info("push message . url:%s body:%s headers:%s", url, str(req), str(headers))
	#client = AsyncHTTPClient()
	#response = yield client.fetch(url, headers=headers, method='POST', body=json.dumps(req))
	response = requests.post(url, data=json.dumps(req), headers=headers)
	if response.status_code != 200:
		error_code = True
		LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
	LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
	return error_code
