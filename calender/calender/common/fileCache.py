#!/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from calender.constants import API_BO, OPEN_API, FILE_SYSTEM

def set_status_by_user_date(user, date, status, check_status):
    bot_no = OPEN_API["botNo"]
    tmp_path = FILE_SYSTEM["cache_dir"] + "/" + str(bot_no) + "/" + user
    status_file = tmp_path + "/" + date + ".status"
    content = {
        "status": status
    }

    if not os.os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    content_str = json.dumps(content)
    if os.os.path.exists(status_file):
        file_handle = open(status_file, mode='r+')
        content = json.loads(file_handle.read())
        if "status" in content and content["status"] not in check_status:
            return False, "check after status failed"
        file_handle.truncate()
        file_handle.write(content_str)
        file_handle.close()
        return True, None

    file_handle = open(status_file, mode='w+')
    file_handle.write(content_str)
    file_handle.close()
    return True, None

def get_status_by_user(user, date):
    bot_no = OPEN_API["botNo"]
    tmp_path = FILE_SYSTEM["cache_dir"] + "/" + str(bot_no) + "/" + user
    status_file = tmp_path + "/" + date + ".status"
    if not os.os.path.exists(status_file):
        return None
    file_handle = open(status_file, mode='w+')
    content = json.loads(file_handle.read())
    file_handle.close()
    if "status" not in content:
        return None
    return content["status"]

def set_schedule_by_user(account_id, date, schedule_id, begin, end):
    bot_no = OPEN_API["botNo"]
    time_zone = API_BO["calendar"]["TZone"]
    tmp_path = FILE_SYSTEM["cache_dir"] + "/" + str(bot_no) + "/" + account_id
    cache_file = tmp_path + "/" + date + ".data"

    content = {
        "schedule_id": schedule_id,
        "begin": begin,
        "end": end,
        "time_zone": time_zone
    }

    if not os.os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    if not os.os.path.exists(cache_file):
        file_handle = open(cache_file, mode='w+')
        file_handle.write(json.dumps(content))
        file_handle.close()
    else:
        return False, "cache file exist"
    return True, None


def get_schedule_by_user(account_id, date):
    bot_no = OPEN_API["botNo"]
    tmp_path = FILE_SYSTEM["cache_dir"] + "/" + str(bot_no) + "/" + account_id
    cache_file = tmp_path + "/" + date + ".data"

    if os.os.path.exists(cache_file):
        file_handle = open(cache_file, mode='r+')
        content_str = file_handle.read()
        file_handle.close()
        return json.loads(content_str)
    else:
        return None

def modify_schedule_by_user(account_id, date, schedule_id, end):
    bot_no = OPEN_API["botNo"]
    tmp_path = FILE_SYSTEM["cache_dir"] + "/" + str(bot_no) + "/" + account_id
    cache_file = tmp_path + "/" + date + ".data"

    if os.os.path.exists(cache_file):

        file_handle = open(cache_file, mode='r+')
        content_str = file_handle.read()
        content = json.loads(content_str)
        file_handle.close()
        if content is None or content["schedule_id"] != schedule_id:
            return False
        content["end"] = end
        file_handle.truncate()
        file_handle.write(json.dumps(content))
        file_handle.close()
    else:
        return False
    return True

def set_calender_id(calender_id):
    bot_no = OPEN_API["botNo"]
    tmp_path = FILE_SYSTEM["cache_dir"] + "/" + str(bot_no)
    cache_file = tmp_path + "/" + "calender_tmp" + ".data"

    content = {"calender_id": calender_id}
    if not os.os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    if not os.os.path.exists(cache_file):
        file_handle = open(cache_file, mode='w+')
        file_handle.write(json.dumps(content))
        file_handle.close()
    else:
        file_handle = open(cache_file, mode='r+')
        content = json.loads(file_handle.read())
        content["calender_id"] = calender_id
        file_handle.truncate()
        file_handle.write(json.dumps(content))
        file_handle.close()

def get_calender_id():
    bot_no = OPEN_API["botNo"]
    tmp_path = FILE_SYSTEM["cache_dir"] + "/" + str(bot_no)
    cache_file = tmp_path + "/" + "calender_tmp" + ".data"
    if not os.os.path.exists(cache_file):
        return None
    file_handle = open(cache_file, mode='r')
    content = json.loads(file_handle.read())
    return content["calender_id"]





