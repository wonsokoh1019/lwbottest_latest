#!/bin/bash python3
# -*- coding: UTF-8 -*-
"""
the global setting for calender
"""
LOG_PATH = "/home1/irteam/logs/calender/"
CALENDER_LOG_FILE = LOG_PATH + "calender.log"
CALENDER_LOG_ROTATE = "midnight"
CALENDER_LOG_FMT = '[%(asctime)-15s] [%(levelname)s] %(filename)s %(funcName)s:%(lineno)d %(process)d %(request_id).8s %(message)s'
CALENDER_LOG_LEVEL = "DEBUG"

CALENDER_PORT = 9090
CALENDER_PID_FILE = LOG_PATH + "calender.pid"
