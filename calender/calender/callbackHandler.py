#!/bin/env python
# -*- coding: utf-8 -*-
"""
internal hello
"""
import logging
import tornado.web
from externals.sendMessage import *
from externals.data import *
from constants import *
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

def check_para(body):

    if body["Type"] != "message":
        return False, "parameter error Type is not message"

    if body["Content"] is None or body["Content"]["Type"] != "text" or body["Content"]["postback"] is None:
        error_code, error_message = first_page(body["accountId"], body["roomId"])
        if not error_code:
            return error_code, error_message
        return sign(body["accountId"], body["roomId"])

    if body["Content"]["postback"] == "sign_in":
        return sign_in(body["accountId"], body["roomId"])

    if body["Content"]["postback"] == "sign_out":
        return sign_out(body["accountId"], body["roomId"])

    if body["Content"]["postback"] == "to_firt":
        return sign(body["accountId"], body["roomId"])

    if body["Content"]["postback"] == "direct_sign_in":
        return direct_sign_in(body["accountId"], body["roomId"])

    if body["Content"]["postback"] == "direct_sign_out":
        return direct_sign_out(body["accountId"], body["roomId"])

    if body["Content"]["postback"] == "manual_sign_in":
        return manual_sign_in(body["accountId"], body["roomId"])

    if body["Content"]["postback"] == "manual_sign_out":
        return manual_sign_out(body["accountId"], body["roomId"])

    if body["Content"]["postback"] == "Previous_step_in":
        return sign_in(body["accountId"], body["roomId"])
    if body["Content"]["postback"] == "Previous_step_out":
        return sign_out(body["accountId"], body["roomId"])
#会发确认
    if body["Content"]["postback"].find("echo_display") != -1:
        return echo_display(body["accountId"], body["roomId"], body["Content"]["postback"], body["Content"]["text"])

    if body["Content"]["postback"].find("confirm") != -1:
        return confirm(body["Content"]["postback"])

    if body["Content"]["postback"].find("rollback") != -1:
        return rollback(body["Content"]["postback"])
    return True, None

def first_page(account_id, room_id):
    cn_text = i18n_text("zh_CN", "欢迎使用calender bot")
    en_text = i18n_text("en_US", "welcome access calender bot")
    kr_text = i18n_text("ko_KR", "calender bot 사용 환영합니다")

    i18n_texts = [cn_text, en_text, kr_text]
    text = make_text("welcome access calender bot", i18n_texts)
    request["accountId"] = account_id
    request["roomId"] = room_id
    request["BotNo"] = OPEN_API["botNo"]
    request["content"] = text
    headers = {
        "Content-Type":"application/json",
        "charset":"UTF-8"
    }
    error_code = send_message(request, headers)
    if error_code:
        LOGGER.error("send_message step1 failed. room_id:%d account_id:%ld", room_id, account_id)
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

    action1 = make_postback_action("sign", "Punch the clock", "Punch the clock", sign_labels, sign_text)

    column1 = make_image_carousel_column("https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png",
                                             "", action1, sign_images)

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

    action2 = make_postback_action("sync_calender", "sync calender", "sync calender", sync_labels, sync_text)

    column2 = make_image_carousel_column("https://static.worksmobile.net/static/wm/botprofile/Bot_kitchen_640.png",
                                         "", action2, sync_calender_images)

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
    action3 = make_postback_action("check calender", "check_calender", "check calender", check_labels, check_text)

    column3 = make_image_carousel_column("https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png",
                                         "", action3, check_calender_images)
    columns = [column1, column2, column3]
    image_carousel = make_image_carousel(columns)

    request["content"] = image_carousel

    error_code = send_message(request, headers)
    if error_code:
        LOGGER.error("send_message step2 failed. room_id:%d account_id:%ld", room_id, account_id)
        return False, "send message failed."
    return True, None
def sign(account_id, room_id):

    size = make_size(2500, 1686)
    bound1 = make_bound(0, 0, 1250, 843)

    cn_text1 = i18n_display_text("zh_CN", "上班打卡")
    en_text1 = i18n_display_text("en_US", "Get work records")
    kr_text1 = i18n_display_text("ko_KR", "출근 기록 가져오기")
    display_text1 = [cn_text1, en_text1, kr_text1]
    action1 = make_postback_action("sign_in", display_text1)

    bound2 = make_bound(0, 843, 1250, 1686)
    cn_text2 = i18n_display_text("zh_CN", "下班打卡")
    en_text2 = i18n_display_text("en_US", "Get off-duty records")
    kr_text2 = i18n_display_text("ko_KR", "퇴근 기록 가져오기")
    display_text2 = [cn_text2, en_text2, kr_text2]

    action2 = make_postback_action("sign_out", display_text2)

    bound3 = make_bound(1250, 0, 2500, 1686)
    cn_text3 = i18n_display_text("zh_CN", "回到首页")
    en_text3 = i18n_display_text("en_US", "Back to the front page")
    kr_text3 = i18n_display_text("ko_KR", "홈페이지로 돌아오다")
    display_text3 = [cn_text3, en_text3, kr_text3]

    action3 = make_postback_action("to_firt", display_text3)

    rich_menu = make_rich_menu("https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png",
                   size,
                   [make_area(bound1, action1),make_area(bound2, action2),make_area(bound3, action3)])

    request["accountId"] = account_id
    request["roomId"] = room_id
    request["BotNo"] = OPEN_API["botNo"]
    request["content"] = rich_menu
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    error_code = send_message(request, headers)
    if error_code:
        LOGGER.error("send_message step2 failed. room_id:%d account_id:%ld", room_id, account_id)
        return False, "send message failed."

    return True, None

def sign_in(account_id, room_id):
    cn_text = make_i18n_content_texts("zh_CN", "请选择录入上班时间的方式")
    en_text = make_i18n_content_texts("en_US", "Please choose the way to enter working hours.")
    kr_text = make_i18n_content_texts("ko_KR", "출근 시간 선택")
    content_texts = [cn_text, en_text, kr_text]

    cn_text1 = i18n_display_text("zh_CN", "以当前时间录入上班时间")
    en_text1 = i18n_display_text("en_US", "Enter working hours at the current time")
    kr_text1 = i18n_display_text("ko_KR", "당면 시간으로 출근 시간.")
    display_text1 = [cn_text1, en_text1, kr_text1]
    action1 = make_postback_action("direct_sign_in", display_text1)

    cn_text2 = i18n_display_text("zh_CN", "直接录入上班时间")
    en_text2 = i18n_display_text("en_US", "Direct entry of working hours")
    kr_text2 = i18n_display_text("ko_KR", "바로 출근 시간")
    display_text2 = [cn_text2, en_text2, kr_text2]
    action2 = make_postback_action("manual_sign", display_text2)

    button = make_button("Please choose the way to enter working hours", content_texts,[action1, action2])
    request["accountId"] = account_id
    request["roomId"] = room_id
    request["BotNo"] = OPEN_API["botNo"]
    request["content"] = button
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    error_code = send_message(request, headers)
    if error_code:
        LOGGER.error("send_message step2 failed. room_id:%d account_id:%ld", room_id, account_id)
        return False, "send message failed."

    return True,None
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
    request["accountId"] = account_id
    request["roomId"] = room_id
    request["BotNo"] = OPEN_API["botNo"]
    request["content"] = button
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    error_code = send_message(request, headers)
    if error_code:
        LOGGER.error("send_message step2 failed. room_id:%d account_id:%ld", room_id, account_id)
        return False, "send message failed."

    return True, None

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
    action1 = make_postback_action("confirm_in", display_text3)

    cn_text2 = i18n_text("zh_CN", "上一步")
    en_text2 = i18n_text("en_US", "Previous step")
    kr_text2 = i18n_text("ko_KR", "전보")
    display_text2 = [cn_text2, en_text2, kr_text2]
    action2 = make_postback_action("Previous_step_in", display_text2)
    reply_item1 = make_quick_reply_item(action1, "https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png")
    reply_item2 = make_quick_reply_item(action2, "https://static.worksmobile.net/static/wm/botprofile/Bot_Dice_640.png")

    text["quickReply"] = {reply_item1, reply_item2}

    request["accountId"] = account_id
    request["roomId"] = room_id
    request["BotNo"] = OPEN_API["botNo"]
    request["content"] = text
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    error_code = send_message(request, headers)
    if error_code:
        LOGGER.error("send_message step2 failed. room_id:%d account_id:%ld", room_id, account_id)
        return False, "send message failed."

    return True, None

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

    request["accountId"] = account_id
    request["roomId"] = room_id
    request["BotNo"] = OPEN_API["botNo"]
    request["content"] = text
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    error_code = send_message(request, headers)
    if error_code:
        LOGGER.error("send_message step2 failed. room_id:%d account_id:%ld", room_id, account_id)
        return False, "send message failed."

    return True, None

def manual_sign_in(account_id, room_id):
    LOGGER.info("account_id:%s, room_id:%s",str(account_id), str(room_id))
    return True, None

def manual_sign_out(account_id, room_id):
    LOGGER.info("account_id:%s, room_id:%s",str(account_id), str(room_id))
    return True, None

def echo_display(account_id, room_id, postback, text):
    LOGGER.info("account_id:%s, room_id:%s postback:%s text:%s",str(account_id), str(room_id), postback, text)
    return True, None

def confirm_in(account_id, room_id):
    LOGGER.info("account_id:%s, room_id:%s", str(account_id), str(room_id))
    return True, None

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
    def post(self):
        """
        support post
        """

        path = self.request.uri
        LOGGER.info("request para path:%s", path)

        post_data = self.request.body_arguments

        LOGGER.info("request para body:%s", str(post_data))
        error_code, error_message = check_para(body)
        if not error_code:
            raise tornado.web.HTTPError(403, error_message)
        self.finish()
