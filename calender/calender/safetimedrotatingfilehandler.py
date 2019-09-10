#!/bin/env python3
# -*- encoding:UTF-8  -*-

"""
multi-process safe timed rotating file handler
"""

import os
import time
from logging.handlers import TimedRotatingFileHandler
from filelock import FileLock

class SafeTimedRotatingFileHandler(TimedRotatingFileHandler):
    """safe timed rotating file handler for multi-process"""
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        """constructor"""
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc)
    def doRollover(self):
        """override doRollover for multi-process safe"""
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        current_time = int(time.time())
        dst_now = time.localtime(current_time)[-1]
        tmptime = self.rolloverAt - self.interval
        if self.utc:
            time_tuple = time.gmtime(tmptime)
        else:
            time_tuple = time.localtime(tmptime)
            dst_then = time_tuple[-1]
            if dst_now != dst_then:
                if dst_now:
                    addend = 3600
                else:
                    addend = -3600
                time_tuple = time.localtime(tmptime + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, time_tuple)
        #if os.path.exists(dfn):
        #    os.remove(dfn)
        # Issue 18940: A file may not have been created if delay is True.
        lock = FileLock(self.baseFilename + ".lock")
        with lock:
            if os.path.exists(self.baseFilename) and not os.path.exists(dfn):
                os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for iterfiles in self.getFilesToDelete():
                os.remove(iterfiles)
        if not self.delay:
            self.mode = "a"
            self.stream = self._open()
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                if not dst_now:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                new_rollover_at += addend
        self.rolloverAt = new_rollover_at
