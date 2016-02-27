#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap

from config import DebugConfig

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(DebugConfig)

@app.route('/', methods=['GET'])
def main_handler():
    return 'Hello'

