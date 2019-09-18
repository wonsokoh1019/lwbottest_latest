#!/bin/env python
# -*- coding: utf-8 -*-
import io
import logging
import socket
from data import *
from tornado.httpclient import AsyncHTTPClient

sys.path.append('../')

from constants import API_BO, OPEN_API

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

def send_message(req, headers):
	error_code = False
	headers["consumerKey"] = OPEN_API["consumerKey"]
	headers["Authorization"] = "Bearer " + OPEN_API["token"]

	url = API_BO["url"]
	url.replace("API_ID", OPEN_API["apiId"])
	client = AsyncHTTPClient()
	response = yield client.fetch(url, headers=headers, method='POST', body=json.dumps(req))
	if response.code != 200:
		error_code = True
		LOGGER.info("send message failed.")
	LOGGER.info("send message failed. body:%s", str(response.body))
	return error_code