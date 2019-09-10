#!/bin/bash python3
# -*- coding: UTF-8 -*-
"""
constants.py Defining the constant used for a project.

"""
import os

# ---------------------------------------------------------------------
# Constants and global variables
# ---------------------------------------------------------------------
ABSDIR_OF_SELF           = os.path.dirname(os.path.abspath(__file__))
LOG_CONF_FILE            = ABSDIR_OF_SELF + '/log.conf'
ABSDIR_OF_PARENT         = os.path.dirname(ABSDIR_OF_SELF)

NGINX_SERVER             = "http://127.0.0.1:8080/"
