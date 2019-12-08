#!/bin/env python
# -*- coding: utf-8 -*-
"""
create i18n message content
"""

import json
from attendance_management_bot.constant import IMAGE_CAROUSEL
from attendance_management_bot.model.data import *
import gettext
import locale
_ = gettext.gettext


def get_i18n_content(fmt, local, **kw):
    ko = gettext.translation(local, 'locales', ['ko'])
    en = gettext.translation(local, 'locales', ['en'])
    ja = gettext.translation(local, 'locales', ['ja'])

    i18n_content = {}
    function = None
    if 'function' in kw:
        function = kw['function']
        if function is not None:
            i18n_content = []

    fmt1 = None
    if 'fmt1' in kw:
        fmt1 = kw['fmt1']

    date = None
    if 'date' in kw:
        date = kw['date']

    for lang in [('en_US', en), ('ja_JP', ja), ('ko_KR', ko)]:
        if fmt1 is not None and date is not None:
            locale.setlocale(locale.LC_TIME,
                             "{lang}{code}".format(lang=lang[0], code=".utf8"))
            kw['date'] = date.strftime(lang[1].gettext(fmt1))

        if function is not None:
            if len(kw) > 0:
                i18n_content_item = function(lang[0],
                                             lang[1].gettext(fmt).format(**kw))
            else:
                i18n_content_item = function(lang[0],
                                             lang[1].gettext(fmt))

            i18n_content.append(i18n_content_item)
        elif len(kw) > 0:
            i18n_content[lang[0]] = lang[1].gettext(fmt).format(**kw)
        else:
            i18n_content[lang[0]] = lang[1].gettext(fmt)
    return i18n_content


def get_i18n_content_by_lang(fmt, fmt2, local, lang, **kw):

    local_map = {'en': 'en_US', 'ja': 'ja_JP', 'kr': 'ko_KR'}
    local_text = gettext.translation(local, 'locales', [lang])

    date = None
    if 'date' in kw:
        date = kw['date']

    if date:
        locale.setlocale(locale.LC_TIME,
                         "{lang}{code}".format(lang=local_map[lang],
                                               code=".utf8"))
        kw['date'] = date.strftime(local_text.gettext(fmt2))
    if len(kw) > 0:
        return local_text.gettext(fmt).format(**kw)
    return local_text.gettext(fmt)


def make_i18n_button(text, actions, local, fmt):
    i18n_texts = get_i18n_content(fmt, local, function=make_i18n_content_texts)
    return make_button(text, actions, content_texts=i18n_texts)


def make_i18n_text(text, local, fmt, **kw):
    i18n_texts = get_i18n_content(fmt, local, function=i18n_text, **kw)
    return make_text(text, i18n_texts=i18n_texts)


def make_i18n_message_action(post_back, local, label, fmt_label=None,
                             text=None, fmt_text=None):
    i18n_labels = None
    if fmt_label is not None:
        i18n_labels = get_i18n_content(fmt_label, local, function=make_i18n_label)

    i18n_texts = None
    if fmt_text is not None:
        i18n_texts = get_i18n_content(fmt_text, local, function=i18n_text)
    return make_message_action(post_back, label, i18n_labels=i18n_labels,
                               text=text, i18n_texts=i18n_texts)


def make_i18n_postback_action(post_back, local, label, fmt_label=None,
                              text=None, fmt_text=None):
    i18n_labels = None
    if fmt_label is not None:
        i18n_labels = get_i18n_content(fmt_label, local, function=make_i18n_label)

    i18n_texts = None
    if fmt_text is not None:
        i18n_texts = get_i18n_content(fmt_text, local, function=i18n_display_text)

    return  make_postback_action(post_back, label, i18n_labels,
                                 text, i18n_texts)


def make_il8n_image_carousel_column(number, action):
    i18n_images = []
    for lang in [('en_US', 'en'), ('ja_JP', 'ja'), ('ko_KR', 'ko')]:
        i18n_image_item = make_i18n_image_url(lang[0],
                                              IMAGE_CAROUSEL[lang[1]][number])
        i18n_images.append(i18n_image_item)

    return make_image_carousel_column(image_url=IMAGE_CAROUSEL['en'][number],
                                      action=action,
                                      i18n_image_urls=i18n_images)

