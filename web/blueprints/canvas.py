# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect
from web.domain import RegisterEventForm

FB_APP_URL = 'https://apps.facebook.com/952096844837567/'

canvas = Blueprint('canvas', __name__, template_folder='templates', url_prefix='/')


@canvas.route('/', methods=['GET'])
def redirect_to_fb_app():
    return redirect(FB_APP_URL, code=302)


@canvas.route('/', methods=['POST'])
def canvas_home():
    form = RegisterEventForm()
    return render_template('index.html', form=form)
