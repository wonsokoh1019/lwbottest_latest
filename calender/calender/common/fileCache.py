#!/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from calender.constant import API_BO, OPEN_API, FILE_SYSTEM


def set_status_by_user_date(user, date, status=None, process=None,
                            delete_flag=False):
    bot_no = OPEN_API["botNo"]
    tmp_path = FILE_SYSTEM["cache_dir"] + "/" + str(bot_no) + "/" + user
    status_file = tmp_path + "/" + date + ".status"
    content = {}
    if status is not None:
        content["status"] = status
    if process is not None:
        content["process"] = process

    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    content_str = json.dumps(content)
    if os.path.exists(status_file):
        file_handle = open(status_file, mode='r+')
        old_content = file_handle.read()
        old_content_json = {}
        if old_content is not None:
            old_content_json = json.loads(old_content)
        if status is not None:
            old_content_json["status"] = status
        elif delete_flag:
            del old_content_json["status"]
        if process is not None:
            old_content_json["process"] = process
        file_handle.seek(0)
        file_handle.truncate()
        file_handle.write(json.dumps(old_content_json))
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
    if not os.path.exists(status_file):
        return None
    file_handle = open(status_file, mode='r+')
    content_str = file_handle.read()
    if content_str is None:
        file_handle.close()
        return None
    content = json.loads(content_str)
    file_handle.close()
    return content


def clean_status_by_user(user, date):
    bot_no = OPEN_API["botNo"]
    tmp_path = FILE_SYSTEM["cache_dir"] + "/" + str(bot_no) + "/" + user
    cache_file = tmp_path + "/" + date + ".data"
    status_file = tmp_path + "/" + date + ".status"
    if os.path.exists(status_file):
        os.remove(status_file)
    if os.path.exists(cache_file):
        os.remove(cache_file)


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

    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    if not os.path.exists(cache_file):
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

    if os.path.exists(cache_file):
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

    if os.path.exists(cache_file):

        file_handle = open(cache_file, mode='r+')
        content_str = file_handle.read()
        content = None
        if content_str is not None:
            content = json.loads(content_str)
        if content is None or content["schedule_id"] != schedule_id:
            file_handle.close()
            return False
        content["end"] = end
        file_handle.seek(0)
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
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    if not os.path.exists(cache_file):
        file_handle = open(cache_file, mode='w+')
        file_handle.write(json.dumps(content))
        file_handle.close()
    else:
        file_handle = open(cache_file, mode='r+')
        content_str = file_handle.read()
        if content_str is None:
            file_handle.close()
            return False
        content = json.loads(content_str)
        content["calender_id"] = calender_id
        file_handle.seek(0)
        file_handle.truncate()
        file_handle.write(json.dumps(content))
        file_handle.close()
        return True


def get_calender_id():
    bot_no = OPEN_API["botNo"]
    tmp_path = FILE_SYSTEM["cache_dir"] + "/" + str(bot_no)
    cache_file = tmp_path + "/" + "calender_tmp" + ".data"
    if not os.path.exists(cache_file):
        return None
    file_handle = open(cache_file, mode='r')
    content_str = file_handle.read()
    if content_str is None:
        file_handle.close()
        return None
    content = json.loads(file_handle.read())
    file_handle.close()
    return content["calender_id"]
