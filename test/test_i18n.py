# -*- coding: utf-8 -*-

import gettext
_ = gettext.gettext

def get_data():
    return _("Hello, I'm an attendance management "
             "bot of LINE WORKS that helps your "
             "timeclock management and entry.")

def test_ko():
    original = get_data()
    ko = gettext.translation('base', 'locales', ['ko'])
    en = gettext.translation('base', 'locales', ['en'])
    ja = gettext.translation('base', 'locales', ['ja'])
    assert ko.gettext(original).startswith(u'안녕하세요')
    assert ja.gettext(original).startswith(u'こんにちは。')
    assert en.gettext(original).startswith('Hello, ')
