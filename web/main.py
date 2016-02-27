#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from config import DebugConfig
from blueprints import *

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(DebugConfig)


app.register_blueprint(blueprint=events)


@app.route('/', methods=['GET'])
def main_handler():
    return 'Hello'

