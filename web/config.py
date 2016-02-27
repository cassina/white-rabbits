# -*- coding: utf-8 -*-
import os


class DebugConfig(object):
    SECRET_KEY = os.getenv('KEY')
    DEBUG = True
    TESTING = False

