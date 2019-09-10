#!/bin/env python
# -*- coding: utf-8 -*-
"""
internal hello
"""
import logging
import tornado.web
LOGGER = logging.getLogger("calender")
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
        post_data = self.request.body_arguments
        LOGGER.info("post_data: %s", str(post_data))
        self.finish()
