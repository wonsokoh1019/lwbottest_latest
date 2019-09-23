#! /bin/bash python3
# -*- coding: utf-8 -*-
"""
launch calender
"""
import os
import logging
import logging.handlers
import asyncio
import uvloop
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options
from calender.externals.richmenu import *
from calender.common import globalData
from calender.externals.data import *
from calender.constants import API_BO

import psutil

import calender.router
import calender.contextlog
import calender.safetimedrotatingfilehandler
from calender.settings import CALENDER_PORT, CALENDER_LOG_FMT, CALENDER_LOG_LEVEL, CALENDER_LOG_FILE, CALENDER_LOG_ROTATE

define("port", default=CALENDER_PORT, help="server listen port. default 9090")
define("workers", default=0, help="the count of workers. default the same as cpu cores")
define("logfile", default=None, help="the path for log")

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def sigHandler(sig, _):
    """
    signal handler
    """
    print("sig %s received"% str(sig))
    try:
        parent = psutil.Process(os.getpid())
        children = parent.children()
        for process in children:
            process.send_signal(sig)
    except (psutil.NoSuchProcess, psutil.ZombieProcess, psutil.AccessDenied) as ex:
        print(str(ex))
    tornado.ioloop.IOLoop.instance().add_callback(killServer)

def killServer():
    """
    stop the ioloop
    """
    asyncio.get_event_loop().stop()
    #tornado.ioloop.IOLoop.instance().stop()

def initLogger():
    """
    init logger setting
    """
    #access_log = logging.getLogger("tornado.access")

    formatter = logging.Formatter(CALENDER_LOG_FMT)
    calender_log = logging.getLogger("calender")
    file_handler = calender.safetimedrotatingfilehandler.SafeTimedRotatingFileHandler(
        filename=CALENDER_LOG_FILE,
        when=CALENDER_LOG_ROTATE,
    )
    file_handler.setFormatter(formatter)

    calender_log.setLevel(CALENDER_LOG_LEVEL)
    file_handler.addFilter(calender.contextlog.RequestContextFilter())
    calender_log.addHandler(file_handler)

    # add app/gen ERROR log
    logging.getLogger("tornado.application").addHandler(file_handler)
    logging.getLogger("tornado.general").addHandler(file_handler)

def initRichMenu():
    rich_menu_id = init_rich_menu(API_BO["rich_menu"]["name"])
    if rich_menu_id is None:
        LOGGER = logging.getLogger("calender")
        LOGGER.info("init rich menu failed.")
    else:
        globalData.set_value(API_BO["rich_menu"]["name"], rich_menu_id)

def startCalender():
    """
    the calender launch code
    """
    server = tornado.httpserver.HTTPServer(calender.router.getRouter())
    server.bind(options.port)
    server.start(options.workers)

    initLogger()
    initRichMenu()
    
    asyncio.get_event_loop().run_forever()
    #tornado.ioloop.IOLoop.instance().start()
    server.stop()
    #tornado.ioloop.IOLoop.instance().stop()
    asyncio.get_event_loop().close()

    print("exit...")
