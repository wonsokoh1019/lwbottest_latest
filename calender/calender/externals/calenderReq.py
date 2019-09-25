#!/bin/env python
# -*- coding: utf-8 -*-
import io
import logging
import json
from calender.externals.data import *
from calender.constants import API_BO, OPEN_API, ADMIN_ACCOUNT
import tornado.gen
from calender.common.fileCache import *
import requests
import uuid

def create_headers():
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    headers["Authorization"] = "Bearer " + OPEN_API["token"]
    return headers

def make_icalender_data(begin, end, current, account_id, careate_flag=False):
    uid = str(uuid.uuid4()) + account_id
    schedule_lcal_string = "BEGIN:VCALENDAR\r\n"
    schedule_lcal_string = schedule_lcal_string + "VERSION:2.0\r\n"
    schedule_lcal_string = schedule_lcal_string + "PRODID:Naver Calendar\r\n"
    schedule_lcal_string = schedule_lcal_string + "CALSCALE:GREGORIAN\r\n"
    schedule_lcal_string = schedule_lcal_string + "BEGIN:VTIMEZONE\r\n"
    schedule_lcal_string = schedule_lcal_string + "TZID:Asia/Seoul\r\n"
    schedule_lcal_string = schedule_lcal_string + "BEGIN:STANDARD\r\n"
    schedule_lcal_string = schedule_lcal_string + "DTSTART:19700101T000000\r\n"
    schedule_lcal_string = schedule_lcal_string + "TZNAME:GMT+09:00\r\n"
    schedule_lcal_string = schedule_lcal_string + "TZOFFSETFROM:+0900\r\n"
    schedule_lcal_string = schedule_lcal_string + "TZOFFSETTO:+0900\r\n"
    schedule_lcal_string = schedule_lcal_string + "END:STANDARD\r\n"
    schedule_lcal_string = schedule_lcal_string + "END:VTIMEZONE\r\n"
    schedule_lcal_string = schedule_lcal_string + "BEGIN:VEVENT\r\n"
    schedule_lcal_string = schedule_lcal_string + "SEQUENCE:0\r\n"
    schedule_lcal_string = schedule_lcal_string + "CLASS:PUBLIC\r\n"

    schedule_lcal_string = schedule_lcal_string + "TRANSP:OPAQUE\r\n"
    if careate_flag:
        schedule_lcal_string = schedule_lcal_string + "UID:" + uid + "\r\n"
    schedule_lcal_string = schedule_lcal_string + "DTSTART;TZID=Asia/Seoul:" + begin + "\r\n"
    schedule_lcal_string = schedule_lcal_string + "DTEND;TZID=Asia/Seoul:" + end + "\r\n"
    schedule_lcal_string = schedule_lcal_string + "SUMMARY:Punch of"+account_id+"\r\n"
    schedule_lcal_string = schedule_lcal_string + "LOCATION:Here\r\n"
    schedule_lcal_string = schedule_lcal_string + "RRULE:FREQ=WEEKLY;BYDAY=FR;INTERVAL=1;UNTIL=20141030T120000\r\n"
    schedule_lcal_string = schedule_lcal_string + "RRULE:FREQ=WEEKLY;BYDAY=FR;INTERVAL=1;UNTIL=20141030T120000\r\n"
    if careate_flag:
        schedule_lcal_string = schedule_lcal_string + "CREATED:"+ current +"\r\n"
    schedule_lcal_string = schedule_lcal_string + "LAST-MODIFIED:" + current + "\r\n"
    schedule_lcal_string = schedule_lcal_string + "DTSTAMP:" + current + "\r\n"
    schedule_lcal_string = schedule_lcal_string + "END:VEVENT\r\n"
    schedule_lcal_string = schedule_lcal_string + "END:VCALENDAR\r\n"

    return schedule_lcal_string

def create_calender():
    body =  {
        "name": API_BO["calendar"]["name"],
        "desc": "Punch schedule",
        "invitationMapListJson": {
            "email": ADMIN_ACCOUNT,
            "actionType": insert
            #"roleId": "2"
        }
    }
    headers = create_headers()
    url = API_BO["calendar"]["create_calender_url"]
    LOGGER.info("create calender . url:%s body:%s", url, str(body))

    response = requests.post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return None

    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        return None
    return tmp["returnValue"]

def get_calenders(time): #syncToken (yyyyMMddHHmmss).
    headers = create_headers()
    url = API_BO["calendar"]["get_calenders_url"]
    if time is not None:
        url = url + "?syncToken=" + time
    LOGGER.info("create calender . url:%s body:%s", url, str(body))

    response = requests.GET(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return None

    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    return json.loads(response.content)

def create_schedules(calendar_id, begin, end, current, account_id):
    body = {"calendarId":calendar_id, "scheduleIcalString":make_icalender_data(begin, end, current, account_id, True)}

    headers = create_headers()
    url = API_BO["calendar"]["create_schedule_url"]
    LOGGER.info("create calender . url:%s body:%s", url, str(body))

    response = requests.post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return None

    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        return None
    return tmp["returnValue"]

def modify_schedules(calendar_id, begin, end, current, account_id):

    body = {"calendarId":calendar_id, "scheduleIcalString":make_icalender_data(begin, end, current, account_id)}

    headers = create_headers()
    url = API_BO["calendar"]["modify_schedule_url"]
    LOGGER.info("create calender . url:%s body:%s", url, str(body))

    response = requests.post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s", url, response.text, response.content)
        return None

    LOGGER.info("push message success. url:%s txt:%s body:%s", url, response.text, response.content)
    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        return None
    return tmp["returnValue"]

def init_calender():
    calender_id = get_calender_id(OPEN_API["botNo"])
    if calender_id is not None:
        return calender_id
    calender_id = create_calender()
    if calender_id is not None:
        set_calender_id(OPEN_API["botNo"], calender_id)
        return calender_id
    return None





