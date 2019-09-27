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
        error_message, content = yield deal_message(account_id, body["content"]["text"])
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
            or (body["type"] == "message" and "content" in body and "text" in body["content"] and  body["content"]["text"] == "start") \
            or (body["type"] == "postback" and "data" in body and body["data"] == "to_firt") :
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
        clean_status_by_user(account_id, date)
        error_code, error_message = yield sign(account_id)
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
            set_status_by_user_date(account_id, current_date, "sign_in_done")
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
            set_status_by_user_date(account_id, current_date, "sign_out_done")
            return error_code, error_message
        return success, content

    return False, "can't deal message"
@tornado.gen.coroutine
def first_message():
    cn_text = i18n_text("zh_CN", "欢迎使用calender bot")
    en_text = i18n_text("en_US", "welcome access calender bot")
    kr_text = i18n_text("ko_KR", "안녕하세요, 출퇴근 시간을 입력하고관리할 수 있도록 도와드리는 라인웍스의管理出勤bot 입니다.")

    i18n_texts = [cn_text, en_text, kr_text]

    text = make_text("안녕하세요, 출퇴근 시간을 입력하고관리할 수 있도록 도와드리는 라인웍스의管理出勤bot 입니다.", i18n_texts)
    return text

@tornado.gen.coroutine
def image_interduce():
    action1 = make_postback_action("aaa", label="aaa")
    column1 = make_image_carousel_column(image_resource_id=API_BO["image_carousel"]["resource_id"][0], action=action1)

    action2 = make_postback_action("bbb", label="bbb")
    column2 = make_image_carousel_column(image_resource_id=API_BO["image_carousel"]["resource_id"][1],action=action2)

    action3 = make_postback_action("ccc", label="ccc")
    column3 = make_image_carousel_column(image_resource_id=API_BO["image_carousel"]["resource_id"][2], action=action3)

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
def sign_in():
    cn_text = make_i18n_content_texts("zh_CN", "请选择录入上班时间的方式")
    en_text = make_i18n_content_texts("en_US", "Please choose the way to enter working hours.")
    kr_text = make_i18n_content_texts("ko_KR", "출근 시간 선택")
    content_texts = [cn_text, en_text, kr_text]

    cn_text1 = make_i18n_label("zh_CN", "当前时间")
    en_text1 = make_i18n_label("en_US", "Enter current time")
    kr_text1 = make_i18n_label("ko_KR", "당면 ")
    display_label1 = [cn_text1, en_text1, kr_text1]
    action1 = make_message_action("시간으로", "direct_sign_in", i18n_labels=display_label1)

    cn_text2 = make_i18n_label("zh_CN", "直接录入")
    en_text2 = make_i18n_label("en_US", "Direct entry")
    kr_text2 = make_i18n_label("ko_KR", "바로")
    display_label2 = [cn_text2, en_text2, kr_text2]
    action2 = make_message_action("바로", "manual_sign_in", i18n_labels=display_label2)

    return make_button("출근 시간 선택", [action1, action2], content_texts=content_texts)

@tornado.gen.coroutine
def sign_out():
    cn_text = make_i18n_content_texts("zh_CN", "请选择录入下班时间的方式")
    en_text = make_i18n_content_texts("en_US", "Please choose the way to enter the off-duty time.")
    kr_text = make_i18n_content_texts("ko_KR", "퇴근 시간 채택 해주세요")
    content_texts = [cn_text, en_text, kr_text]

    cn_text1 = make_i18n_label("zh_CN", "当前时间")
    en_text1 = make_i18n_label("en_US", "Enter current time")
    kr_text1 = make_i18n_label("ko_KR", "시간으로 퇴근")
    display_label1 = [cn_text1, en_text1, kr_text1]
    action1 = make_message_action("시간으로", "direct_sign_out", i18n_labels=display_label1)

    cn_text2 = make_i18n_label("zh_CN", "直接录入")
    en_text2 = make_i18n_label("en_US", "Direct entry")
    kr_text2 = make_i18n_label("ko_KR", "바로")
    display_label2 = [cn_text2, en_text2, kr_text2]
    action2 = make_message_action("바로","manual_sign_out", i18n_labels=display_label2)

    return make_button("퇴근 시간 채택 해주세요", [action1, action2], content_texts=content_texts)
@tornado.gen.coroutine
def deal_sign_in(sign_time, manual_falg = False):
    # todo
    #获取当前时间
    #一并显示
    call_back = "sign_in"
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sign_time))
    if manual_falg:
        call_back = "manual_sign_in"

    cn_text = i18n_text("zh_CN", "是否要用这个时间签到？ 时间:" + current_time)
    en_text = i18n_text("en_US", "Do you want to check in at the this time? time:" + current_time)
    kr_text = i18n_text("ko_KR", "이 시간에 서명해야 합니까? 시간:" + current_time)

    text = make_text("이 시간에 서명해야 합니까? 이 시간:" + current_time, [cn_text, en_text, kr_text])

    cn_text3 = make_i18n_label("zh_CN", "确定")
    en_text3 = make_i18n_label("en_US", "yes")
    kr_text3 = make_i18n_label("ko_KR", "확정")
    display_label = [cn_text3, en_text3, kr_text3]
    action1 = make_postback_action("confirm_in&time="+str(sign_time), label = "확정", i18n_labels = display_label, display_text = "확정?")

    cn_text2 = make_i18n_label("zh_CN", "上一步")
    en_text2 = make_i18n_label("en_US", "Previous step")
    kr_text2 = make_i18n_label("ko_KR", "전보")
    display_label2 = [cn_text2, en_text2, kr_text2]
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
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sign_time))
    if manual_falg:
        call_back = "manual_sign_out"

    cn_text = i18n_text("zh_CN", "是否要用这个时间签退？ 时间:" + current_time)
    en_text = i18n_text("en_US", "Do you want to sign back at the current time? current time:" + current_time)
    kr_text = i18n_text("ko_KR", "이 시간에 서명해야 합니까? 시간:" + current_time)

    text = make_text("현재 시간으로 서명해야 합니까? 현재 시간:" + current_time, [cn_text, en_text, kr_text])

    cn_text3 = make_i18n_label("zh_CN", "确定")
    en_text3 = make_i18n_label("en_US", "yes")
    kr_text3 = make_i18n_label("ko_KR", "확정")
    display_label = [cn_text3, en_text3, kr_text3]
    action1 = make_postback_action("confirm_out&time="+str(current_time_tickt),  label = "확정", i18n_labels = display_label, display_text = "확정?")

    cn_text2 = make_i18n_label("zh_CN", "上一步")
    en_text2 = make_i18n_label("en_US", "Previous step")
    kr_text2 = make_i18n_label("ko_KR", "전보")
    display_label2 = [cn_text2, en_text2, kr_text2]
    action2 = make_postback_action(call_back, label = "전보", i18n_labels = display_label2, display_text = "전보?")
    reply_item1 = make_quick_reply_item(action1)
    reply_item2 = make_quick_reply_item(action2)

    content = text
    content["quickReply"] = make_quick_reply([reply_item1, reply_item2])
    return content

def reminder_message():
    cn_text = i18n_text("zh_CN", "您已经签到（或者签退）成功，请不要重复输入")
    en_text = i18n_text("en_US", "You have successfully checked in (or checked out). Please do not type again.")
    kr_text = i18n_text("ko_KR", "이미 서명 (또는 서명) 에 성공하였으니, 중복 입력하지 마십시오")

    i18n_texts1 = [cn_text, en_text, kr_text]

    text = make_text("이미 서명 (또는 서명) 에 성공하였으니, 중복 입력하지 마십시오", i18n_texts1)
    return text

@tornado.gen.coroutine
def manual_sign_in(account_id, create_time):
    yield from asyncio.sleep(1)
    current_date = time.strftime("%Y-%m-%d", time.localtime(create_time))
    cn_text = i18n_text("zh_CN", "请直接输入上班时间")
    en_text = i18n_text("en_US", "Please enter the working hours directly")
    kr_text = i18n_text("ko_KR", "바로 출근 시간 입력해주세요")

    i18n_texts1 = [cn_text, en_text, kr_text]

    text1 = make_text("바로 출근 시간 입력해주세요", i18n_texts1)

    cn_text = i18n_text("zh_CN", "输入时间时，请按顺序填写4位数字。例如，如果想填写下午8点20分的话，请填写2020的数字。")
    en_text = i18n_text("en_US", "When entering time, please fill in 4 digits in order.For example, if you want to fill in at 8:20 p.m., please fill in the number of 2020.")
    kr_text = i18n_text("ko_KR", "시간을 입력 하실 때는 총 4자리 숫자를 시,분 순서대로 기입해 주세요.예를 들어, 오후 8시 20분을 기입 하고 싶으시면 2020 이라는 숫자를 작성해 주시면 됩니다.")

    i18n_texts2 = [cn_text, en_text, kr_text]
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
    cn_text = i18n_text("zh_CN", "请直接输入下班时间")
    en_text = i18n_text("en_US", "Please enter the closing time directly.")
    kr_text = i18n_text("ko_KR", "퇴근 시간 바로 입력해주세요.")

    i18n_texts1 = [cn_text, en_text, kr_text]

    text1 = make_text("퇴근 시간 바로 입력해주세요", i18n_texts1)

    cn_text = i18n_text("zh_CN", "输入时间时，请按顺序填写4位数字。例如，如果想填写下午8点20分的话，请填写2020的数字。")
    en_text = i18n_text("en_US",
                        "When entering time, please fill in 4 digits in order.For example, if you want to fill in at 8:20 p.m., please fill in the number of 2020.")
    kr_text = i18n_text("ko_KR",
                        "시간을 입력 하실 때는 총 4자리 숫자를 시,분 순서대로 기입해 주세요.예를 들어, 오후 8시 20분을 기입 하고 싶으시면 2020 이라는 숫자를 작성해 주시면 됩니다.")

    i18n_texts2 = [cn_text, en_text, kr_text]
    text2 = make_text(
        "시간을 입력 하실 때는 총 4자리 숫자를 시,분 순서대로 기입해 주세요.예를 들어, 오후 8시 20분을 기입 하고 싶으시면 2020 이라는 숫자를 작성해 주시면 됩니다.",
        i18n_texts2)

    set_status_by_user_date(account_id, current_date, "wait_out")
    return {"first": text1, "seconde": text2}

@tornado.gen.coroutine
def error_message():
    cn_text = i18n_text("zh_CN", "对不起.我没有理解你写的时间。再确认一下你的方法然后输入时间.")
    en_text = i18n_text("en_US", "I'm sorry. I didn't understand the time you wrote. Confirm your method again and enter the time.")
    kr_text = i18n_text("ko_KR", "죄송합니다.  작성하신 시간을 이해하지 못하였습니다. 다시 한번 录入 방법을 확인하시고 시간을 입력해 주세요. ")

    i18n_texts1 = [cn_text, en_text, kr_text]

    text1 = make_text("퇴근 시간 바로 입력해주세요", i18n_texts1)

    cn_text = i18n_text("zh_CN", "输入时间时，请按顺序填写4位数字。例如，如果想填写下午8点20分的话，请填写2020的数字。")
    en_text = i18n_text("en_US",
                        "When entering time, please fill in 4 digits in order.For example, if you want to fill in at 8:20 p.m., please fill in the number of 2020.")
    kr_text = i18n_text("ko_KR",
                        "시간을 입력 하실 때는 총 4자리 숫자를 시,분 순서대로 기입해 주세요.예를 들어, 오후 8시 20분을 기입 하고 싶으시면 2020 이라는 숫자를 작성해 주시면 됩니다.")

    i18n_texts2 = [cn_text, en_text, kr_text]
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

    cn_text = i18n_text("zh_CN", "签到成功")
    en_text = i18n_text("en_US", "Sign in successfully")
    kr_text = i18n_text("ko_KR", "성공에 서명하다")

    text = make_text("성공에 서명하다", [cn_text, en_text, kr_text])
    return True, text

@tornado.gen.coroutine
def confirm_out(account_id, callback):
    pos = callback.find("time=")
    str_time = callback[pos:]
    my_time = int(str_time)

    current_date = time.strftime("%Y-%m-%d", time.localtime(my_time))
    # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(my_time))

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

    hours = (my_time - begin_time)/3600
    min = ((my_time - begin_time) % 3600)/60

    cn_text = i18n_text("zh_CN", "签退成功，您上班用时 "+hours+"小时 " + min + "分")
    en_text = i18n_text("en_US", "Sign-out is successful. It takes you "+hours+" hours "+min+"minutes to go to work.")
    kr_text = i18n_text("ko_KR", "체결에 성공하면 출근 시 "+hours+"시간 "+min+"나누다")

    text = make_text("체결에 성공하면 출근 시 8시간", [cn_text, en_text, kr_text])
    return True, text

@tornado.gen.coroutine
def deal_message(account_id, message, create_time):

    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
    status = get_status_by_user(account_id, current_date)

    if status is None:
        LOGGER.info("status is None account_id:%s message:%s", account_id, message)
        return "failed", None
    try:
        user_time = int(message)
    except Exception as e:
        if status == "wait_in" or status == "wait_out":
            content = yield error_message()
            #clean_status_by_user(account_id, current_date)
            return "error_message", content
        else:
            return "failed", None
    
    tm = (local_time.tm_year, local_time.tm_mon, local_time.tm_mday, int(user_time/100), int(user_time%100), 00, local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst)

    user_time_ticket = int(time.mktime(tm))

    if (status == "wait_in" or status == "wait_out") and (user_time < 0 or user_time > 2400):
        content = yield error_message()
        #clean_status_by_user(account_id, current_date)
        return "error_message", content

    if status == "wait_in":
        set_status_by_user_date(account_id, current_date, "in_done")
        content =  yield deal_sign_in(user_time_ticket, True)
        return "success", content
    elif status == "wait_out":
        set_status_by_user_date(account_id, current_date, "out_done")
        content =  yield deal_sign_out(user_time_ticket, True)
        return "success", content
    elif status == "sign_in_done" or status == "sign_out_done":
        return "success", reminder_message()
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
