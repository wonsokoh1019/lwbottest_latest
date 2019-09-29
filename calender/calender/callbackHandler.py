#!/bin/env python
# -*- coding: utf-8 -*-
"""
internal hello
"""
import logging
import tornado.web
import time
import asyncio
from calender.externals.sendMessage import push_message
from calender.common import globalData
from calender.externals.richmenu import *
from calender.externals.calenderReq import *
from calender.constants import API_BO
from calender.externals.data import *
from calender.common import globalData
from calender.common.fileCache import *
from calender.constants import *

LOGGER = logging.getLogger("calender")

"""
type CustomerCallbackV2Request_Content struct {
	Type       string   `json:"type"`
	Text       *string  `json:"text,omitempty"`
	Postback   *string  `json:"postback,omitempty"`
	Address    *string  `json:"address,omitempty"`   // location
	Latitude   *float64 `json:"latitude,omitempty"`  // location
	Longitude  *float64 `json:"longitude,omitempty"` // location
	PackageId  *string  `json:"packageId,omitempty"` // sticker
	StickerId  *string  `json:"stickerId,omitempty"` // sticker
	ResourceId *string  `json:"resourceId,omitempty"`
}

type CustomerCallbackV2Request struct {
	Type string `json:"type"`
	Data string `json:"data,omitempty"`
	Source struct {
		AccountId *string `json:"accountId,omitempty"`
		RoomId    *string `json:"roomId,omitempty"`
	} `json:"source"`
	CreatedTime int64                              `json:"createdTime"`
	Content     *CustomerCallbackV2Request_Content `json:"content,omitempty"`
	MemberList  *[]string                          `json:"memberList,omitempty"`
	UserKey     *common.UserKey                    `json:"userKey,omitempty"`
}
"""
cmd_messge = ["start", "manual_sign_out", "manual_sign_in", "direct_sign_out", "direct_sign_in", "sign_out", "sign_in"]

en_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
kr_week = ["월요일","화요일","수요일","목요일","금요일","토요일","일요일"]
jp_week = ["月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日"]

en_month = ["January","February","March","April","May","June","July","August","September","October","November","December"]
#kr_month = ["일월","이월","삼월","사월","오월","유월","칠월","팔월","구월","시월","십이월","십이월"]
#jp_month = ["いちがつ", "にがつ", "さんがつ", "しがつ", "ごがつ", "ろくがつ", "しちがつ", "はちがつ", "くがつ", "じゅうがつ", "じゅういちがつ", "じゅうにがつ"]

status_value = {
    "wait_in":1,
    "in_done":2,
    "sign_in_done":3,
    "wait_out":4,
    "out_done":5,
    "sign_out_done":6
}

def check_is_messge_time(message):
    if message in cmd_messge or message.find("confirm_out") != -1 or message.find("confirm_in") != -1:
        return False
    return True

@tornado.gen.coroutine
def check_para(body):
    LOGGER.info("begin deal check_para")
    error_message = None
    request = {}
    if body is None or "source" not in body or "accountId" not in body["source"] or "createdTime" not in body:
        return False, "parameter error."

    account_id = body["source"].get("accountId", None)
    room_id = body["source"].get("roomId", None)

    create_time = time.time()
    if account_id is not None:
        request["accountId"] = account_id
    elif room_id is not None:
        request["roomId"] = room_id

    if  body["type"] == "message" and "type" in body["content"] and body["content"]["type"] == "text" \
            and "postback" not in body["content"] and "text" in body["content"] and check_is_messge_time(body["content"]["text"]):
        LOGGER.info("begin to deal room_id:%s account_id:%s", str(room_id), str(account_id))
        error_message, content = yield deal_message(account_id, body["content"]["text"], create_time)
        if error_message == "error_message":
            if content is None:
                LOGGER.info("yield error_message failed. room_id:%s account_id:%s", str(room_id), str(account_id))
                return False, "send message failed."

            request["content"] = content["first"]
            error_code = yield push_message(request)
            if error_code:
                LOGGER.info("yield error_message failed. room_id:%s account_id:%s", str(room_id), str(account_id))
                return False, "error_message failed."

            request["content"] = content["seconde"]
            error_code = yield push_message(request)
            if error_code:
                LOGGER.info("yield error_message failed. room_id:%s account_id:%s", str(room_id), str(account_id))
                return False, "send message failed."
            return error_code, error_message
        elif error_message == "success":
            if content is None:
                LOGGER.info("yield message failed. room_id:%s account_id:%s", str(room_id), str(account_id))
                return False, "deal message failed."
            request["content"] = content
            error_code = yield push_message(request)
            if error_code:
                LOGGER.info("yield sgin in failed. room_id:%s account_id:%s", str(room_id), str(account_id))
                return False, "send message failed."
            return error_code, error_message
        else:
            return False, "deal error message."

    elif (body["type"] == "message" and "postback" in body["content"] and body["content"]["postback"] == "start") \
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and  body["content"]["text"] == "start"):
        request["content"] = yield first_message()
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield first_message failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."

        request["content"] = yield image_interduce()
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield first_message failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."

        date = time.strftime("%Y-%m-%d", time.localtime(create_time))
        #clean_status_by_user(account_id, date)
        error_code, error_message = yield sign(account_id)
        return error_code, error_message
    elif (body["type"] == "message" and "content" in body and "text" in body["content"] and  body["content"]["text"] == "to_firt") \
            or (body["type"] == "postback" and "data" in body and body["data"] == "to_firt") :
        request["content"] = yield to_first()
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield to_first failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."

        date = time.strftime("%Y-%m-%d", time.localtime(create_time))
        #clean_status_by_user(account_id, date)
        return error_code, error_message
    elif (body["type"] == "postback" and "data" in body and body["data"] == "sign_in") \
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and  body["content"]["text"] == "sign_in"):
        request["content"] = yield sign_in()
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield sgin in failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."
        return error_code, error_message

    if (body["type"] == "postback" and "data" in body and body["data"] == "sign_out") \
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and  body["content"]["text"] == "sign_out"):
        request["content"] =  yield sign_out()
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("sign_out failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."
        return error_code, error_message

    if (body["type"] == "postback" and "data" in body and body["data"] == "to_first") \
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and  body["content"]["text"] == "sign_out"):
        error_code, error_message = yield sign(account_id)
        return error_code, error_message

    if (body["type"] == "postback" and "data" in body and body["data"] == "direct_sign_in") \
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and  body["content"]["text"] == "direct_sign_in") \
            or (body["type"] == "message" and "content" in body and "postback" in body["content"] and body["content"]["postback"] == "direct_sign_in"):

        request["content"] = yield deal_sign_in(create_time)
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield direct sgin in failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."
        return error_code, error_message

    if (body["type"] == "postback" and "data" in body and body["data"] == "direct_sign_out") \
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and  body["content"]["text"] == "direct_sign_out") \
            or (body["type"] == "message" and "content" in body and "postback" in body["content"] and body["content"]["postback"] == "direct_sign_out"):
        request["content"] = yield deal_sign_out(create_time)
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield direct sgin out failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."
        return error_code, error_message

    if (body["type"] == "postback" and "data" in body and body["data"] == "manual_sign_in") \
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and  body["content"]["text"] == "manual_sign_in") \
            or (body["type"] == "message" and "content" in body and "postback" in body["content"] and body["content"]["postback"] == "manual_sign_in"):
        content = yield manual_sign_in(account_id)
        if content is None:
            LOGGER.info("yield manual_sign_in failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "manual_sign_in failed."
        request["content"] = content["first"]
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield manual_sign_in failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."

        request["content"] = content["seconde"]
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield manual_sign_in failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."
        return error_code, error_message

    if (body["type"] == "postback" and "data" in body and body["data"] == "manual_sign_out") \
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and  body["content"]["text"] == "manual_sign_out") \
            or (body["type"] == "message" and "content" in body and "postback" in body["content"] and body["content"]["postback"] == "manual_sign_out"):
        content = yield manual_sign_out(account_id)
        if content is None:
            LOGGER.info("yield manual_sign_out failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "manual_sign_out failed."
        request["content"] = content["first"]
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield manual_sign_out failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."

        request["content"] = content["seconde"]
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield manual_sign_out failed. room_id:%s account_id:%s", str(room_id), str(account_id))
            return False, "send message failed."
        return error_code, error_message
#会发确认
    if (body["type"] == "postback" and "data" in body and body["data"].find("confirm_in") != -1) \
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and body["content"]["text"].find("confirm_in") != -1):
        if "data" in body and body["data"].find("confirm_in") != -1:
            message = body["data"]
        else:
            message = body["content"]["text"]
        success, content = yield confirm_in(account_id, message)
        if success:
            request["content"] = content
            error_code = yield push_message(request)
            if error_code:
                LOGGER.info("yield confirm_in failed. room_id:%s account_id:%s", str(room_id), str(account_id))
                return False, "send message failed."
            set_status_by_user_date(account_id, current_date, process="sign_in_done")
            return error_code, error_message
        return success, content

    if (body["type"] == "postback" and "data" in body and body["data"].find("confirm_out") != -1) \
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and body["content"]["text"].find("confirm_out") != -1):
        if "data" in body and body["data"].find("confirm_out") != -1:
            message = body["data"]
        else:
            message = body["content"]["text"]
        success, content = yield confirm_out(account_id, message)
        if success:
            request["content"] = content
            error_code = yield push_message(request)
            if error_code:
                LOGGER.info("yield confirm_out failed. room_id:%s account_id:%s", str(room_id), str(account_id))
                return False, "send message failed."
            set_status_by_user_date(account_id, current_date, process="sign_out_done")
            return error_code, error_message
        return success, content

    return False, "can't deal message"
@tornado.gen.coroutine
def first_message():
    jp_text = i18n_text("ko_KR", "공유 캘린더에서 \n모든 직원의 근태 기록을 한눈에 \n확인해볼 수 있습니다")
    en_text = i18n_text("en_US", "Hello, I'm an attendance management bot \nof LINE WORKS that helps \nyour timeclock management and entry.")
    kr_text = i18n_text("ja_JP", "こんにちは。出退勤の時間を入力して \n管理できるようサポートするLINE WORKSの \n勤怠管理Botです。")

    i18n_texts = [jp_text, en_text, kr_text]

    text = make_text("공유 캘린더에서 \n모든 직원의 근태 기록을 한눈에 \n 확인해볼 수 있습니다", i18n_texts)
    return text

def to_first():
    jp_text = i18n_text("ko_KR", "출근, 퇴근하실 때 하단 메뉴에서 \r각각에 맞는 ‘기록하기’ 버튼을 선택해 주세요")
    en_text = i18n_text("en_US", "Please select \"Record\" on the bottom of the menu \neach time when you clock in and clock out.")
    kr_text = i18n_text("ja_JP", "出勤、退勤するときに下のメニューから \rそれぞれ「記録する」ボタンを選択してください。")

    i18n_texts = [jp_text, en_text, kr_text]

    text = make_text("출근, 퇴근하실 때 하단 메뉴에서 \r각각에 맞는 ‘기록하기’ 버튼을 선택해 주세요", i18n_texts)
    return text

@tornado.gen.coroutine
def image_interduce():
    resource_kr0 = make_i18n_image_resource_id("ko_KR", API_BO["image_carousel"]["resource_id"]["ko_KR"][0])
    resource_en0 = make_i18n_image_resource_id("en_US", API_BO["image_carousel"]["resource_id"]["en_US"][0])
    resource_jp0 = make_i18n_image_resource_id("ja_JP", API_BO["image_carousel"]["resource_id"]["ja_JP"][0])
    i18n_resource0 = [resource_kr0, resource_en0, resource_jp0]

    jp_text0 = make_i18n_label("ja_JP", "今使ってみてください")
    en_text0 = make_i18n_label("en_US", "Try it now")
    kr_text0 = make_i18n_label("ko_KR", "지금 사용해 보세요")
    display_label0 = [jp_text0, en_text0, kr_text0]

    display_text_jp0 = i18n_display_text("ja_JP", "ボタンをクリックするだけで簡単に出退勤時間を記録することができます。")
    display_text_en0 = i18n_display_text("en_US", "Timeclock can be recorded easily just by clicking buttons")
    display_text_kr0 = i18n_display_text("ko_KR", "버튼 클릭만으로 손쉽게 출퇴근  시간을 기록할 수 있습니다")
    i18n_display_text0 = [display_text_jp0, display_text_en0, display_text_kr0]
    action1 = make_postback_action("a", display_text="버튼 클릭만으로 손쉽게 출퇴근  시간을 기록할 수 있습니다",
                                   i18n_display_texts = i18n_display_text0, label="지금 사용해 보세요", i18n_labels=display_label0)

    column1 = make_image_carousel_column(image_resource_id=API_BO["image_carousel"]["resource_id"]["ko_KR"][0], i18n_image_resource_ids = i18n_resource0, action=action1)

    resource_kr1 = make_i18n_image_resource_id("ko_KR", API_BO["image_carousel"]["resource_id"]["ko_KR"][1])
    resource_en1 = make_i18n_image_resource_id("en_US", API_BO["image_carousel"]["resource_id"]["en_US"][1])
    resource_jp1 = make_i18n_image_resource_id("ja_JP", API_BO["image_carousel"]["resource_id"]["ja_JP"][1])
    i18n_resource1 = [resource_kr1, resource_en1, resource_jp1]

    display_text_jp1 = i18n_display_text("ja_JP", "入力された勤怠記録は、共有カレンダー に自動で入力されます。")
    display_text_en1 = i18n_display_text("en_US", "Entered attendance records are automatically entered in Shared Calendar")
    display_text_kr1 = i18n_display_text("ko_KR", "입력된 근태 기록은 공유 캘린더에  자동으로 입력됩니다")
    i18n_display_text1 = [display_text_jp1, display_text_en1, display_text_kr1]

    action2 = make_postback_action("b",  display_text="입력된 근태 기록은 공유 캘린더에  자동으로 입력됩니다",
                                   i18n_display_texts = i18n_display_text1, label="지금 사용해 보세요", i18n_labels=display_label0)
    column2 = make_image_carousel_column(image_resource_id=API_BO["image_carousel"]["resource_id"]["ko_KR"][1], i18n_image_resource_ids = i18n_resource1, action=action2)

    resource_kr2 = make_i18n_image_resource_id("ko_KR", API_BO["image_carousel"]["resource_id"]["ko_KR"][2])
    resource_en2 = make_i18n_image_resource_id("en_US", API_BO["image_carousel"]["resource_id"]["en_US"][2])
    resource_jp2 = make_i18n_image_resource_id("ja_JP", API_BO["image_carousel"]["resource_id"]["ja_JP"][2])
    i18n_resource2 = [resource_kr2, resource_en2, resource_jp2]

    display_text_jp2 = i18n_display_text("ja_JP", "勤怠管理共有カレンダーで \nすべての社員の勤怠記録を \n一目で確認できます。")
    display_text_en2 = i18n_display_text("en_US",
                                         "Attendance records of all employees \ncan be checked at a glance via \n Attendance Management Shared Calendar")
    display_text_kr2 = i18n_display_text("ko_KR", "공유 캘린더에서 \n모든 직원의 근태 기록을 한눈에 \n확인해볼 수 있습니다")
    i18n_display_text2 = [display_text_jp2, display_text_en2, display_text_kr2]

    action3 = make_postback_action("c", display_text="공유 캘린더에서 \n모든 직원의 근태 기록을 한눈에 \n확인해볼 수 있습니다",
                                   i18n_display_texts = i18n_display_text2, label="지금 사용해 보세요", i18n_labels=display_label0)
    column3 = make_image_carousel_column(image_resource_id=API_BO["image_carousel"]["resource_id"]["ko_KR"][2], i18n_image_resource_ids = i18n_resource2, action=action3)

    columns = [column1, column2, column3]
    return  make_image_carousel(columns)

@tornado.gen.coroutine
def sign(account_id):
    if account_id is None:
        LOGGER.error("account_id is None.")
        return False
    rich_menu_id = globalData.get_value(API_BO["rich_menu"]["name"], None)
    if rich_menu_id is None:
        LOGGER.error("get rich_menu_id failed.")
        return False, "get rich_menu_id failed."

    return set_user_specific_rich_menu(rich_menu_id, account_id)

@tornado.gen.coroutine
def sign_in(create_time):

    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
    content = get_status_by_user(user, current_date)
    if "process" in content and (content["process"] == "sign_in_done" or content["process"] == "sign_out_done"):
        return reminder_message("sign_in_done")
    jp_text = make_i18n_content_texts("ja_JP", "出勤時間の入力方式を選択してください。")
    en_text = make_i18n_content_texts("en_US", "Register current time as clock-in time")
    kr_text = make_i18n_content_texts("ko_KR", "출근 시간 입력 방식을 선택해 주세요.")
    content_texts = [jp_text, en_text, kr_text]

    jp_text1 = make_i18n_label("ja_JP", "現在時間で出勤を登録する")
    en_text1 = make_i18n_label("en_US", "Enter current time")
    kr_text1 = make_i18n_label("ko_KR", "현재 시간으로 출근 등록하기")
    display_label1 = [jp_text1, en_text1, kr_text1]
    action1 = make_message_action("현재 시간으로 출근 등록하기", "direct_sign_in", i18n_labels=display_label1)

    jp_text2 = make_i18n_label("ja_JP", "出勤時間を直接入力する")
    en_text2 = make_i18n_label("en_US", "Manually enter clock-in time")
    kr_text2 = make_i18n_label("ko_KR", "출근 시간 직접 입력하기")
    display_label2 = [jp_text2, en_text2, kr_text2]
    action2 = make_message_action("출근 시간 직접 입력하기", "manual_sign_in", i18n_labels=display_label2)

    return make_button("출근 시간 입력 방식을 선택해 주세요.", [action1, action2], content_texts=content_texts)

@tornado.gen.coroutine
def sign_out():
    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
    content = get_status_by_user(user, current_date)
    if "process" not in content:
        return reminder_message(None)

    if content["process"] == "sign_out_done":
        return reminder_message("sign_out_done")

    jp_text = make_i18n_content_texts("ja_JP", "退勤時間の入力方式を選択してください。")
    en_text = make_i18n_content_texts("en_US", "Please select the clock-out time entry method.")
    kr_text = make_i18n_content_texts("ko_KR", "퇴근 시간 입력 방식을 선택해 주세요.")
    content_texts = [jp_text, en_text, kr_text]

    jp_text1 = make_i18n_label("ja_JP", "現在時間で退勤を登録する")
    en_text1 = make_i18n_label("en_US", "Register current time as clock-out time")
    kr_text1 = make_i18n_label("ko_KR", "현재 시간으로 퇴근 등록하기")
    display_label1 = [jp_text1, en_text1, kr_text1]
    action1 = make_message_action("현재 시간으로 퇴근 등록하기", "direct_sign_out", i18n_labels=display_label1)

    jp_text2 = make_i18n_label("ja_JP", "退勤時間を直接入力する")
    en_text2 = make_i18n_label("en_US", "Manually enter clock-out time")
    kr_text2 = make_i18n_label("ko_KR", "퇴근 시간 직접 입력하기")
    display_label2 = [jp_text2, en_text2, kr_text2]
    action2 = make_message_action("퇴근 시간 직접 입력하기","manual_sign_out", i18n_labels=display_label2)

    return make_button("퇴근 시간 입력 방식을 선택해 주세요.", [action1, action2], content_texts=content_texts)
@tornado.gen.coroutine
def deal_sign_in(sign_time, manual_falg = False):
    # todo
    #获取当前时间
    #一并显示
    call_back = "sign_in"
    local_time = time.localtime(sign_time)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    if manual_falg:
        call_back = "manual_sign_in"

    week_date_jp = jp_week[local_time.tm_wday]
    week_date_kr = kr_week[local_time.tm_wday]
    week_date_en = en_week[local_time.tm_wday]

    month = str(local_time.tm_mon)
    date = str(local_time.tm_mday)
    min = str(local_time.tm_min)

    interval_jp = "午前"
    interval_en = "AM"
    interval_kr = "오전"

    hours = str(local_time.tm_hour)
    if hours > 12:
        interval_jp = "午後"
        interval_en = "PM"
        interval_kr = "오후"
        hours = hours - 12

    jp_text = i18n_text("ja_JP", "現在時間 "+month+"月 "+date+"日 "+week_date_jp+" "+interval_jp+" "+hours+"時 "+min+"分で出勤時間を登録しますか？")
    en_text = i18n_text("en_US", "Register the current time "+month+", "+date+" "+week_date_en+" at "+hours+":"+min+" "+interval_en+" as clock-out time?")
    kr_text = i18n_text("ko_KR", "현재 시간 "+month+"월 "+date+"일 "+week_date_kr+" "+interval_kr+" "+hours+"시 "+min+"분으로 출근 시간 등록하시겠습니까?")

    text = make_text("이 시간에 서명해야 합니까? 이 시간:" + current_time, [jp_text, en_text, kr_text])

    jp_text3 = make_i18n_label("ja_JP", "はい")
    en_text3 = make_i18n_label("en_US", "yes")
    kr_text3 = make_i18n_label("ko_KR", "예")
    display_label = [jp_text3, en_text3, kr_text3]
    action1 = make_postback_action("confirm_in&time="+str(sign_time), label = "예", i18n_labels = display_label, display_text = "예")

    jp_text2 = make_i18n_label("ja_JP", "いいえ")
    en_text2 = make_i18n_label("en_US", "No")
    kr_text2 = make_i18n_label("ko_KR", "아니요")
    display_label2 = [jp_text2, en_text2, kr_text2]
    action2 = make_postback_action(call_back, label = "전보", i18n_labels = display_label2, display_text = "전보?")
    reply_item1 = make_quick_reply_item(action1)
    reply_item2 = make_quick_reply_item(action2)

    content = text
    content["quickReply"] = make_quick_reply([reply_item1, reply_item2])

    return content

@tornado.gen.coroutine
def deal_sign_out(sign_time, manual_falg = False):
    #todo
    #获取当前时间
    #一并显示
    call_back = "sign_out"
    local_time = time.localtime(sign_time)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    if manual_falg:
        call_back = "manual_sign_out"

    week_date_jp = jp_week[local_time.tm_wday]
    week_date_kr = kr_week[local_time.tm_wday]
    week_date_en = en_week[local_time.tm_wday]

    month = str(local_time.tm_mon)
    date = str(local_time.tm_mday)
    min = str(local_time.tm_min)

    interval_jp = "午前"
    interval_en = "AM"
    interval_kr = "오전"

    hours = str(local_time.tm_hour)
    if hours > 12:
        interval_jp = "午後"
        interval_en = "PM"
        interval_kr = "오후"
        hours = hours - 12

    jp_text = i18n_text("ja_JP", "現在時間 "+month+"月 "+date+"日 "+week_date_jp+" "+interval_jp+" "+hours+"時 "+min+"分で退勤時間を登録しますか？")
    en_text = i18n_text("en_US", "Register the current time "+month+", "+date+" "+week_date_en+" at "+hours+":"+min+" "+interval_en+" as clock-out time?")
    kr_text = i18n_text("ko_KR", "입력하신 "+month+"월 "+date+"일 "+week_date_kr+" "+interval_kr+" "+hours+"시 "+min+"분으로 출근 시간을 등록하시겠습니까?")

    text = make_text("입력하신 "+month+"월 "+date+"일 "+week_date_kr+" "+interval_kr+" "+hours+"시 "+min+"분으로 출근 시간을 등록하시겠습니까?" + current_time, [jp_text, en_text, kr_text])

    jp_text3 = make_i18n_label("ja_JP", "确定")
    en_text3 = make_i18n_label("en_US", "yes")
    kr_text3 = make_i18n_label("ko_KR", "확정")
    display_label = [jp_text3, en_text3, kr_text3]
    action1 = make_postback_action("confirm_out&time="+str(current_time_tickt),  label = "확정", i18n_labels = display_label, display_text = "확정?")

    jp_text2 = make_i18n_label("ja_JP", "上一步")
    en_text2 = make_i18n_label("en_US", "Previous step")
    kr_text2 = make_i18n_label("ko_KR", "전보")
    display_label2 = [jp_text2, en_text2, kr_text2]
    action2 = make_postback_action(call_back, label = "전보", i18n_labels = display_label2, display_text = "전보?")
    reply_item1 = make_quick_reply_item(action1)
    reply_item2 = make_quick_reply_item(action2)

    content = text
    content["quickReply"] = make_quick_reply([reply_item1, reply_item2])
    return content

def reminder_message(process):
    text = None
    if process == "sign_in_process":
        jp_text = i18n_text("ja_JP", "すでに登録済みの出勤時間があります。\n退勤するときに、下のメニューから「退勤を記録する」ボタンを選択してください。")
        en_text = i18n_text("en_US", "There is already a clock-in time. \nPlease select \"Record\" on the bottom of the menu when you clock out.")
        kr_text = i18n_text("ko_KR", "이미 등록된 출근 시간이 있습니다. \n퇴근하실 때, 하단 메뉴에서  ‘퇴근 기록하기’ 버튼을 선택해 주세요.")

        i18n_texts1 = [jp_text, en_text, kr_text]
        text = make_text("이미 등록된 출근 시간이 있습니다. \n퇴근하실 때, 하단 메뉴에서  ‘퇴근 기록하기’ 버튼을 선택해 주세요.", i18n_texts1)

    elif process == "sign_out_process":
        jp_text = i18n_text("ja_JP", "すでに登録済みの退勤時間があります。\n出勤するときに、下のメニューから「出勤を記録する」ボタンを選択してください。")
        en_text = i18n_text("en_US", "There is already a clock-out time.\nPlease select \"Record\" on the bottom of the menu when you clock in.")
        kr_text = i18n_text("ko_KR", "이미 등록된 퇴근 시간이 있습니다.\n출근하실 때, 하단 메뉴에서 ‘출근 기록하기’ 버튼을 선택해 주세요.")

        i18n_texts1 = [jp_text, en_text, kr_text]
        text = make_text("이미 등록된 퇴근 시간이 있습니다.\n출근하실 때, 하단 메뉴에서 ‘출근 기록하기’ 버튼을 선택해 주세요.", i18n_texts1)
    elif process is None:
        jp_text = i18n_text("ja_JP", "今日の出勤時間が登録されていません。下のメニューから「出勤を記録する」ボタンを選択し、先に出勤時間を入力してください。")
        en_text = i18n_text("en_US", "Today's clock-in time has not been registered. Please select \"Record clock-in\" on the bottom of the menu, and enter your clock-in time.")
        kr_text = i18n_text("ko_KR", "오늘의 출근 시간이 등록되어 있지 않습니다. 하단의 메뉴에서 ‘출근 기록하기’ 버튼을 선택하여 출근 시간을 먼저 입력해 주세요.")

        i18n_texts1 = [jp_text, en_text, kr_text]
        text = make_text("오늘의 출근 시간이 등록되어 있지 않습니다. 하단의 메뉴에서 ‘출근 기록하기’ 버튼을 선택하여 출근 시간을 먼저 입력해 주세요.", i18n_texts1)
    return text

def invalid_message():

    jp_text = i18n_text("ja_JP", "テキストを理解していませんでした。出勤、退勤の際下のメニューから \nそれぞれに合った「記録する」ボタンを選択してください。")
    en_text = i18n_text("en_US", "I didn't understand the text. When you go to work or go home, \nPlease select the appropriate \"Record\" button for each.")
    kr_text = i18n_text("ko_KR", "텍스트를 이해하지 못했습니다. 출근, 퇴근하실 때 하단 메뉴에서 \n각각에 맞는 ‘기록하기’ 버튼을 선택해 주세요 .")

    i18n_texts1 = [jp_text, en_text, kr_text]
    text = make_text("이미 등록된 출근 시간이 있습니다. \n퇴근하실 때, 하단 메뉴에서  ‘퇴근 기록하기’ 버튼을 선택해 주세요.", i18n_texts1)

    return text


@tornado.gen.coroutine
def manual_sign_in(account_id, create_time):
    yield from asyncio.sleep(1)
    current_date = time.strftime("%Y-%m-%d", time.localtime(create_time))
    jp_text = i18n_text("ja_JP", "请直接输入上班时间")
    en_text = i18n_text("en_US", "Please enter the working hours directly")
    kr_text = i18n_text("ko_KR", "바로 출근 시간 입력해주세요")

    i18n_texts1 = [jp_text, en_text, kr_text]

    text1 = make_text("바로 출근 시간 입력해주세요", i18n_texts1)

    jp_text = i18n_text("ja_JP", "输入时间时，请按顺序填写4位数字。例如，如果想填写下午8点20分的话，请填写2020的数字。")
    en_text = i18n_text("en_US", "When entering time, please fill in 4 digits in order.For example, if you want to fill in at 8:20 p.m., please fill in the number of 2020.")
    kr_text = i18n_text("ko_KR", "시간을 입력 하실 때는 총 4자리 숫자를 시,분 순서대로 기입해 주세요.예를 들어, 오후 8시 20분을 기입 하고 싶으시면 2020 이라는 숫자를 작성해 주시면 됩니다.")

    i18n_texts2 = [jp_text, en_text, kr_text]
    text2 = make_text("시간을 입력 하실 때는 총 4자리 숫자를 시,분 순서대로 기입해 주세요.예를 들어, 오후 8시 20분을 기입 하고 싶으시면 2020 이라는 숫자를 작성해 주시면 됩니다.", i18n_texts2)

    error_code, error_message = set_status_by_user_date(account_id, current_date, "wait_in")
    if not error_code:
        LOGGER.error("set_status_by_user_date failed.")
        return None
    return {"first":text1,"seconde": text2}

@tornado.gen.coroutine
def manual_sign_out(account_id, create_time):
    yield from asyncio.sleep(1)
    current_date = time.strftime("%Y-%m-%d", time.localtime(create_time))
    jp_text = i18n_text("ja_JP", "请直接输入下班时间")
    en_text = i18n_text("en_US", "Please enter the closing time directly.")
    kr_text = i18n_text("ko_KR", "퇴근 시간 바로 입력해주세요.")

    i18n_texts1 = [jp_text, en_text, kr_text]

    text1 = make_text("퇴근 시간 바로 입력해주세요", i18n_texts1)

    jp_text = i18n_text("ja_JP", "输入时间时，请按顺序填写4位数字。例如，如果想填写下午8点20分的话，请填写2020的数字。")
    en_text = i18n_text("en_US",
                        "When entering time, please fill in 4 digits in order.For example, if you want to fill in at 8:20 p.m., please fill in the number of 2020.")
    kr_text = i18n_text("ko_KR",
                        "시간을 입력 하실 때는 총 4자리 숫자를 시,분 순서대로 기입해 주세요.예를 들어, 오후 8시 20분을 기입 하고 싶으시면 2020 이라는 숫자를 작성해 주시면 됩니다.")

    i18n_texts2 = [jp_text, en_text, kr_text]
    text2 = make_text(
        "시간을 입력 하실 때는 총 4자리 숫자를 시,분 순서대로 기입해 주세요.예를 들어, 오후 8시 20분을 기입 하고 싶으시면 2020 이라는 숫자를 작성해 주시면 됩니다.",
        i18n_texts2)

    set_status_by_user_date(account_id, current_date, "wait_out")
    return {"first": text1, "seconde": text2}

@tornado.gen.coroutine
def error_message():
    jp_text = i18n_text("ja_JP", "申し訳ございません。作成した時間が理解できませんでした。もう一度時間入力の方法を確認し、時間を入力してください。")
    en_text = i18n_text("en_US", "Sorry, but unable to comprehend your composed time. Please check the time entry method again, and enter the time.")
    kr_text = i18n_text("ko_KR", "죄송합니다. 작성하신 시간을 이해하지 못하였습니다. 다시 한 번 시간 입력 방법을 확인하시고 시간을 입력해 주세요.  ")

    i18n_texts1 = [jp_text, en_text, kr_text]

    text1 = make_text("죄송합니다. 작성하신 시간을 이해하지 못하였습니다. 다시 한 번 시간 입력 방법을 확인하시고 시간을 입력해 주세요. ", i18n_texts1)

    jp_text = i18n_text("ja_JP", "時間を入力するときは、合計4桁の数字を時、分の順番に入力してください。\n\n例えば、午後8時20分を入力したい場合は2020という数字を入力してください。")
    en_text = i18n_text("en_US",
                        "Please use the military time format with a total of 4 numerical digits (hhmm) when entering the time.\n\nFor example, type 2020 to indicate 8:20 PM. ")
    kr_text = i18n_text("ko_KR",
                        "시간을 입력하실 때는 총 4자리 숫자를 시,분 순서대로 기재해 주세요.\n\n예를 들어, 오후 8시 20분을 기재 하고 싶으시면 2020이라는 숫자를 작성해 주시면 됩니다.")

    i18n_texts2 = [jp_text, en_text, kr_text]
    text2 = make_text(
        "시간을 입력 하실 때는 총 4자리 숫자를 시,분 순서대로 기입해 주세요.예를 들어, 오후 8시 20분을 기입 하고 싶으시면 2020 이라는 숫자를 작성해 주시면 됩니다.",
        i18n_texts2)

    return {"first": text1, "seconde": text2}

@tornado.gen.coroutine
def confirm_in(account_id, callback):
    pos = callback.find("time=")
    str_time = callback[pos:]
    my_time = int(str_time)

    current_date = time.strftime("%Y-%m-%d", time.localtime(my_time))
    #current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(my_time))

    calender_id = globalData.get_value(API_BO["calendar"]["name"])
    if calender_id is None:
        calender_id = get_calender_id()
        if calender_id is None:
            LOGGER.info("calender_id is None account_id:%s, room_id:%s", str(account_id))
            return False, "calender_id is None."
    my_end_time = my_time + 60
    info = get_schedule_by_user(account_id, date)
    if info is None:
        schedule_id = create_schedules(calendar_id, my_time, my_end_time, my_time, account_id)
        if schedule_id is None:
            LOGGER.info("create_schedules failed account_id:%s, room_id:%s", str(account_id))
            return False, "create schedules failed."
        set_schedule_by_user(account_id, current_date, schedule_id, my_time, my_end_time)
    else:
        LOGGER.info("schedules has exist. account_id:%s, room_id:%s", str(account_id))
        return False, "create schedules failed."

    #set_status_by_user_date(user, date, process="sign_in_done")
    jp_text = i18n_text("ja_JP", "出勤時間の登録が完了しました。")
    en_text = i18n_text("en_US", "Clock-in time has been registered.")
    kr_text = i18n_text("ko_KR", "출근 시간 등록이 완료되었습니다.")

    text = make_text("성공에 서명하다", [jp_text, en_text, kr_text])
    return True, text

@tornado.gen.coroutine
def confirm_out(account_id, callback):
    pos = callback.find("time=")
    str_time = callback[pos:]
    my_time = int(str_time)

    local_time = time.localtime(my_time)

    current_date = time.strftime("%Y-%m-%d", local_time)

    calender_id = globalData.get_value(API_BO["calendar"]["name"])
    if calender_id is None:
        calender_id = get_calender_id()
        if calender_id is None:
            LOGGER.info("calender_id is None account_id:%s, room_id:%s", str(account_id))
            return False, "calender_id is None."
    info = get_schedule_by_user(account_id, date)

    if info is not None:
        schedule_id = info["schedule_id"]
        begin_time = info["begin"]

        if not modify_schedules(calendar_id, begin_time, my_time, my_time):
            LOGGER.info("modify_schedules failed account_id:%s", str(account_id))
        if schedule_id is None:
            LOGGER.info("schedule_id is None account_id:%s", str(account_id))
            return False, "modify schedules failed."
        modify_schedule_by_user(account_id, current_date, schedule_id, my_time)
    else:
        LOGGER.info("schedules has exist. account_id:%s, room_id:%s", str(account_id))
        return False, "create schedules failed."

    #set_status_by_user_date(user, date, process="sign_out_done")

    hours = int((my_time - begin_time)/3600)
    min = ((my_time - begin_time) % 3600)/60
    week_date_jp = jp_week[local_time.tm_wday]
    week_date_kr = kr_week[local_time.tm_wday]
    week_date_en = en_week[local_time.tm_wday]

    month =  str(local_time.tm_mon)
    date = str(local_time.tm_mday)

    jp_text = i18n_text("ja_JP", "退勤時間の登録が完了しました。\n"+month+"月 "+date+"日 "+ week_date_jp+"の合計勤務時間は \n "+str(hours)+"時間 "+str(min)+"分です。")
    en_text = i18n_text("en_US", "Clock-out time has been registered.\nThe total working hours for "+week_date_en+", "+en_month[local_time.tm_mon]+" "+date+" is \n"+str(hours)+" hours and "+str(min)+" minutes.")
    kr_text = i18n_text("ko_KR", "퇴근 시간 등록이 완료되었습니다.\n "+month+"월 "+date+"일 월요일 총 근무 시간은 \n "+str(hours)+"시간 "+str(min)+"분입니다.")

    text = make_text("퇴근 시간 등록이 완료되었습니다.\n "+month+"월 "+date+"일 "+week_date_kr+" 총 근무 시간은 \n "+str(hours)+"시간 "+str(min)+"분입니다.", [jp_text, en_text, kr_text])
    return True, text

@tornado.gen.coroutine
def deal_message(account_id, message, create_time):

    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
    content = get_status_by_user(account_id, current_date)

    if status not in content:
        LOGGER.info("status is None account_id:%s message:%s", account_id, message)
        return "failed", None
    try:
        user_time = int(message)
    except Exception as e:
        if status in content and (content["status"] == "wait_in" or content["status"] == "wait_out"):
            content = yield error_message()
            return "error_message", content
        else:
            return "failed", None
    
    tm = (local_time.tm_year, local_time.tm_mon, local_time.tm_mday, int(user_time/100), int(user_time%100), 00, local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst)

    user_time_ticket = int(time.mktime(tm))

    if "status" in content and (content["status"] == "wait_in" or content["status"] == "wait_out") and (user_time < 0 or user_time > 2400):
        content = yield error_message()
        return "error_message", content

    if "status" in content and content["status"] == "wait_in":
        set_status_by_user_date(account_id, current_date, "in_done")
        content =  yield deal_sign_in(user_time_ticket, True)
        return "success", content
    elif "status" in content and content["status"] == "wait_out":
        set_status_by_user_date(account_id, current_date, "out_done")
        content =  yield deal_sign_out(user_time_ticket, True)
        return "success", content
    elif "process" in content and (content["process"] == "sign_in_done" or content["process"] == "sign_out_done"):
        return "success", invalid_message()
    else:
        LOGGER.info("can't deal this message account_id:%s message:%s status:%s", account_id, message, status)
    return "failed", None
    # todo
    # 获取当前时间
    # 一并显示

class CallbackHandler(tornado.web.RequestHandler):
    """
    /internal/hello
    """
    def get(self):
        """
        support GET
        """
        self.finish()

    @tornado.gen.coroutine
    def post(self):
        """
        support post
        """

        path = self.request.uri
        LOGGER.info("request para path:%s", path)

        post_data = self.request.body

        LOGGER.info("request para body:%s", str(post_data))
        error_code, error_message = yield check_para(json.loads(post_data))
        if not error_code:
            raise tornado.web.HTTPError(403, error_message)
        self.finish()
