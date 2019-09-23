#!/bin/env python
# -*- coding: utf-8 -*-
"""
internal hello
"""
import logging
import tornado.web
from calender.externals.sendMessage import send_message, push_message
from calender.common import globalData
from calender.externals.richmenu import *
from calender.constants import API_BO
from calender.externals.data import *
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

@tornado.gen.coroutine
def check_para(body):
    LOGGER.info("begin deal check_para")
    if body["type"] != "message":
        return False, "parameter error Type is not message"
    error_code = False
    error_message = None
    if body["content"] is None or body["content"]["type"] != "text" or "postback" not in body["content"] or body["content"]["postback"] is None:
        
        #error_code, error_message = yield first_page(body["source"].get("accountId",None), body["source"].get("roomId",None))
        #if not error_code:
        #    return error_code, error_message
        error_code, error_message = yield sign(body["source"].get("accountId",None))
        #error_code, error_message = yield sign_in(body["source"].get("accountId",None), body["source"].get("roomId",None))
        #error_code, error_message = yield direct_sign_in(body["source"].get("accountId",None), body["source"].get("roomId",None))
        return error_code, error_message
    room_id = body["source"].get("roomId",None)
    account_id = body["source"].get("accountId", None)
    if body["content"]["postback"] == "Start":
        error_code, error_message = yield sign(account_id,room_id)
        return error_code, error_message
    if body["content"]["postback"] == "sign_in":
        error_code, error_message = yield sign_in(account_id,room_id)
        return error_code, error_message

    if body["content"]["postback"] == "sign_out":
        error_code, error_message = yield sign_out(account_id,room_id)
        return error_code, error_message

    if body["content"]["postback"] == "to_firt":
        error_code, error_message = yield sign(account_id,room_id)
        return error_code, error_message

    if body["content"]["postback"] == "direct_sign_in":
        error_code, error_message = yield direct_sign_in(account_id,room_id)
        return error_code, error_message

    if body["content"]["postback"] == "direct_sign_out":
        error_code, error_message = yield direct_sign_out(account_id,room_id)
        return error_code, error_message

    if body["content"]["postback"] == "manual_sign_in":
        error_code, error_message = yield manual_sign_in(account_id,room_id)
        return error_code, error_message

    if body["content"]["postback"] == "manual_sign_out":
        error_code, error_message = yield manual_sign_out(account_id,room_id)
        return error_code, error_message

    if body["content"]["postback"] == "Previous_step_in":
        error_code, error_message = yield sign_in(account_id,room_id)
        return error_code, error_message
    if body["content"]["postback"] == "Previous_step_out":
        error_code, error_message = yield sign_out(account_id,room_id)
        return error_code, error_message
#会发确认
    if body["content"]["postback"].find("echo_display") != -1:
        error_code, error_message = yield echo_display(account_id,room_id, body["content"]["postback"], body["content"]["text"])
        return error_code, error_message

    if body["content"]["postback"].find("confirm") != -1:
        error_code, error_message = yield confirm(body["content"]["postback"])
        return error_code, error_message

    if body["content"]["postback"].find("rollback") != -1:
        error_code, error_message = yield rollback(body["content"]["postback"])
        return error_code, error_message
    return True, None

@tornado.gen.coroutine
def first_page(account_id, room_id):
    LOGGER.info("begin deal first_page")
    cn_text = i18n_text("zh_CN", "欢迎使用calender bot")
    en_text = i18n_text("en_US", "welcome access calender bot")
    kr_text = i18n_text("ko_KR", "calender bot 사용 환영합니다")

    i18n_texts = [cn_text, en_text, kr_text]
    text = make_text("welcome access calender bot", i18n_texts)
    request = {}
    if account_id is not None:
        request["accountId"] = account_id
    if room_id is not None:
        request["roomId"] = room_id
    request["BotNo"] = OPEN_API["botNo"]
    request["content"] = text
    headers = {
        "Content-Type":"application/json",
        "charset":"UTF-8"
    }
    error_code = yield send_message(request, headers)
    if error_code:
        LOGGER.info("yield send_message step1 failed. room_id:%s account_id:%s", str(room_id), str(account_id))
        return False, "send message failed."

    cn_sign_image = make_i18n_image_url("zh_CN",
                                         "https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png")
    en_sign_image = make_i18n_image_url("en_US",
                                         "https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png")
    kr_sign_image = make_i18n_image_url("ko_KR",
                                         "https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png")

    sign_images = [cn_sign_image, en_sign_image, kr_sign_image]

    cn_sign_label = make_i18n_label("zh_CN", "打卡")
    en_sign_label = make_i18n_label("en_US", "Punch the clock")
    kr_sign_label = make_i18n_label("ko_KR", "카드를 치다")
    sign_labels = [cn_sign_label, en_sign_label, kr_sign_label]

    cn_sign_text = i18n_display_text("zh_CN", "打卡")
    en_sign_text = i18n_display_text("en_US", "Punch the clock")
    kr_sign_text = i18n_display_text("ko_KR", "카드를 치다")
    sign_text = [cn_sign_text, en_sign_text, kr_sign_text]

    action1 = make_message_action("sign", "Punch the clock", "Punch the clock")

    column1 = make_image_carousel_column("https://alpha-talk.worksmobile.com/p/download/k/oneapp/t/kr1.500/500/4606897.149829238/w320_180", action=action1)
    #column1 = make_image_carousel_column("https://alpha-talk.worksmobile.com/p/download/k/oneapp/t/kr1.500/500/4606897.149829238/w320_180",
    #                                         "", action1, sign_images)

    cn_sync_calender_image = make_i18n_image_url("zh_CN",
                                         "https://static.worksmobile.net/static/wm/botprofile/Bot_kitchen_640.png")
    en_sync_calender_image = make_i18n_image_url("en_US",
                                         "https://static.worksmobile.net/static/wm/botprofile/Bot_kitchen_640.png")
    kr_sync_calender_image = make_i18n_image_url("ko_KR",
                                         "https://static.worksmobile.net/static/wm/botprofile/Bot_kitchen_640.png")

    sync_calender_images = [cn_sync_calender_image, en_sync_calender_image, kr_sync_calender_image]

    cn_sync_label = make_i18n_label("zh_CN", "同步日程")
    en_sync_label = make_i18n_label("en_US", "sync calender")
    kr_sync_label = make_i18n_label("ko_KR", "동기 일정")
    sync_labels = [cn_sync_label, en_sync_label, kr_sync_label]

    cn_sync_text = i18n_display_text("zh_CN", "同步日程")
    en_sync_text = i18n_display_text("en_US", "sync calender")
    kr_sync_text = i18n_display_text("ko_KR", "동기 일정")
    sync_text = [cn_sync_text, en_sync_text, kr_sync_text]

    anction2 = make_postback_action("sync", "sync calender", label="lable")

    column2 = make_image_carousel_column("https://alpha-talk.worksmobile.com/p/download/k/oneapp/t/kr1.500/500/4606897.149829238/w320_180",action=action2)
    #column2 = make_image_carousel_column("https://static.worksmobile.net/static/wm/botprofile/Bot_kitchen_640.png",
    #                                     "", action2, sync_calender_images)

    cn_check_calender_image = make_i18n_image_url("zh_CN",
                                                 "https://static.worksmobile.net/static/wm/botprofile/Bot_General_640.png")
    en_check_calender_image = make_i18n_image_url("en_US",
                                                 "https://static.worksmobile.net/static/wm/botprofile/Bot_General_640.png")
    kr_check_calender_image = make_i18n_image_url("ko_KR",
                                                 "https://static.worksmobile.net/static/wm/botprofile/Bot_General_640.png")

    check_calender_images = [cn_check_calender_image, en_check_calender_image, kr_check_calender_image]

    cn_check_label = make_i18n_label("zh_CN", "查看日程")
    en_check_label = make_i18n_label("en_US", "check calender")
    kr_check_label = make_i18n_label("ko_KR", "일정을 살펴보다")
    check_labels = [cn_check_label, en_check_label, kr_check_label]

    cn_check_text = i18n_display_text("zh_CN", "查看日程")
    en_check_text = i18n_display_text("en_US", "check calender")
    kr_check_text = i18n_display_text("ko_KR", "일정을 살펴보다")
    check_text = [cn_check_text, en_check_text, kr_check_text]
    action3 = make_message_action("check", "check_calender", "check calender")

    column3 = make_image_carousel_column("https://alpha-talk.worksmobile.com/p/download/k/oneapp/t/kr1.500/500/4606897.149829238/w320_180", action=action3)
    #column3 = make_image_carousel_column("https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png",
    #                                     "", action3, check_calender_images)
    columns = [column1, column2, column3]
    image_carousel = make_image_carousel(columns)

    request["content"] = image_carousel

    error_code = yield push_message(request, headers)
    if error_code:
        LOGGER.error("yield send_message step2 failed. room_id:%d account_id:%d", room_id, account_id)
        return False, "send message failed."
    return True, None

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
def sign_in(account_id, room_id):
    cn_text = make_i18n_content_texts("zh_CN", "请选择录入上班时间的方式")
    en_text = make_i18n_content_texts("en_US", "Please choose the way to enter working hours.")
    kr_text = make_i18n_content_texts("ko_KR", "출근 시간 선택")
    content_texts = [cn_text, en_text, kr_text]

    cn_text1 = i18n_text("zh_CN", "以当前时间录入上班时间")
    en_text1 = i18n_text("en_US", "Enter working hours at the current time")
    kr_text1 = i18n_text("ko_KR", "당면 시간으로 출근 시간.")
    display_text1 = [cn_text1, en_text1, kr_text1]
    action1 = make_message_action("direct_sign_in","direct_sign_in", "current", i18n_texts=display_text1)

    cn_text2 = i18n_text("zh_CN", "直接录入上班时间")
    en_text2 = i18n_text("en_US", "Direct entry of working hours")
    kr_text2 = i18n_text("ko_KR", "바로 출근 시간")
    display_text2 = [cn_text2, en_text2, kr_text2]
    action2 = make_message_action("manual_sign","manual_sign", "entry", i18n_texts=display_text2)

    button = make_button("Please choose the way to enter working hours", [action1, action2], content_texts=content_texts)
    request = {}
    if account_id is not None:
         request["accountId"] = account_id
    if room_id is not None:
         request["roomId"] = room_id
    request["BotNo"] = OPEN_API["botNo"]
    request["content"] = button
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    error_code = yield push_message(request, headers)
    if error_code:
        LOGGER.error("yield send_message step2 failed. room_id:%d account_id:%ld", room_id, account_id)
        return False, "send message failed."

    return True,None

@tornado.gen.coroutine
def sign_out(account_id, room_id):
    cn_text = make_i18n_content_texts("zh_CN", "请选择录入下班时间的方式")
    en_text = make_i18n_content_texts("en_US", "Please choose the way to enter the off-duty time.")
    kr_text = make_i18n_content_texts("ko_KR", "퇴근 시간 채택 해주세요.")
    content_texts = [cn_text, en_text, kr_text]

    cn_text1 = i18n_display_text("zh_CN", "以当前时间录入下班时间")
    en_text1 = i18n_display_text("en_US", "Enter off time at current time")
    kr_text1 = i18n_display_text("ko_KR", "현재 시간으로 퇴근 시간.")
    display_text1 = [cn_text1, en_text1, kr_text1]
    action1 = make_postback_action("direct_sign_out", display_text1)

    cn_text2 = i18n_display_text("zh_CN", "直接录入下班时间")
    en_text2 = i18n_display_text("en_US", "Direct entry of off hours")
    kr_text2 = i18n_display_text("ko_KR", "바로 퇴근 시간.")
    display_text2 = [cn_text2, en_text2, kr_text2]
    action2 = make_postback_action("manual_out", display_text2)

    make_button("Please choose the way to enter working hours", content_texts, [action1, action1])

    button = make_button("Please choose the way to enter working hours", content_texts, [action1, action2])
    request = {}
    if account_id is not None:
         request["accountId"] = account_id
    if room_id is not None:
         request["roomId"] = room_id
    request["BotNo"] = OPEN_API["botNo"]
    request["content"] = button
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    error_code = yield push_message(request, headers)
    if error_code:
        LOGGER.error("yield send_message step2 failed. room_id:%d account_id:%ld", room_id, account_id)
        return False, "send message failed."

    return True, None
@tornado.gen.coroutine
def direct_sign_in(account_id, room_id):
    # todo
    #获取当前时间
    #一并显示
    cn_text = i18n_text("zh_CN", "是否要用当前时间签到？")
    en_text = i18n_text("en_US", "Do you want to check in at the current time?")
    kr_text = i18n_text("ko_KR", "현재 시간으로 서명해야 합니까?")

    text = make_text("Do you want to check in at the current time?", [cn_text, en_text, kr_text])

    cn_text3 = i18n_text("zh_CN", "确定")
    en_text3 = i18n_text("en_US", "yes")
    kr_text3 = i18n_text("ko_KR", "확정")
    display_text3 = [cn_text3, en_text3, kr_text3]
    action1 = make_postback_action("confirm_in", "confirm_in", "confirm_in")

    cn_text2 = i18n_text("zh_CN", "上一步")
    en_text2 = i18n_text("en_US", "Previous step")
    kr_text2 = i18n_text("ko_KR", "전보")
    display_text2 = [cn_text2, en_text2, kr_text2]
    action2 = make_postback_action("Previous_step_in", "Previous_step_in", "Previous_step_in")
    reply_item1 = make_quick_reply_item(action1)
    reply_item2 = make_quick_reply_item(action2)
    content = text
    content["quickReply"] = make_quick_reply([reply_item1, reply_item2])
    request = {}
    if account_id is not None:
         request["accountId"] = account_id
    if room_id is not None:
         request["roomId"] = room_id
    #request["BotNo"] = OPEN_API["botNo"]
    
    request["content"] = content
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    error_code = yield push_message(request, headers)
    if error_code:
        LOGGER.error("yield send_message step2 failed. room_id:%d account_id:%ld", room_id, account_id)
        return False, "send message failed."

    return True, None

@tornado.gen.coroutine
def direct_sign_out(account_id, room_id):
    #todo
    #获取当前时间
    #一并显示
    cn_text = i18n_text("zh_CN", "是否要用当前时间签退？")
    en_text = i18n_text("en_US", "Do you want to sign back at the current time?")
    kr_text = i18n_text("ko_KR", "현재 시간으로 서명해야 합니까?")

    text = make_text("Do you want to sign back at the current time?", [cn_text, en_text, kr_text])

    cn_text3 = i18n_text("zh_CN", "确定")
    en_text3 = i18n_text("en_US", "yes")
    kr_text3 = i18n_text("ko_KR", "확정")
    display_text3 = [cn_text3, en_text3, kr_text3]
    action1 = make_postback_action("confirm_out", display_text3)

    cn_text2 = i18n_text("zh_CN", "上一步")
    en_text2 = i18n_text("en_US", "Previous step")
    kr_text2 = i18n_text("ko_KR", "전보")
    display_text2 = [cn_text2, en_text2, kr_text2]
    action2 = make_postback_action("Previous_step_out", display_text2)
    reply_item1 = make_quick_reply_item(action1, "https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png")
    reply_item2 = make_quick_reply_item(action2, "https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png")

    text["quickReply"] = {reply_item1, reply_item2}

    request = {}
    if account_id is not None:
         request["accountId"] = account_id
    if room_id is not None:
         request["roomId"] = room_id
    request["BotNo"] = OPEN_API["botNo"]
    request["content"] = text
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    error_code = yield send_message(request, headers)
    if error_code:
        LOGGER.error("yield send_message step2 failed. room_id:%d account_id:%ld", room_id, account_id)
        return False, "send message failed."

    return True, None

@tornado.gen.coroutine
def manual_sign_in(account_id, room_id):
    LOGGER.info("account_id:%s, room_id:%s",str(account_id), str(room_id))
    return True, None

@tornado.gen.coroutine
def manual_sign_out(account_id, room_id):
    LOGGER.info("account_id:%s, room_id:%s",str(account_id), str(room_id))
    return True, None

@tornado.gen.coroutine
def echo_display(account_id, room_id, postback, text):
    LOGGER.info("account_id:%s, room_id:%s postback:%s text:%s",str(account_id), str(room_id), postback, text)
    return True, None

@tornado.gen.coroutine
def confirm_in(account_id, room_id):
    LOGGER.info("account_id:%s, room_id:%s", str(account_id), str(room_id))
    return True, None

@tornado.gen.coroutine
def confirm_out(account_id, room_id):
    LOGGER.info("account_id:%s, room_id:%s", str(account_id), str(room_id))
    return True, None

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
