#!/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./')
from calendar_bot.initDB import init_db
from calendar_bot.registerBot import init_bot


def main():
    init_db()
    init_bot()


if __name__ == "__main__":
    main()
