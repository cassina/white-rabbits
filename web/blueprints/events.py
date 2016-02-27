# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

events = Blueprint('events', __name__, template_folder='templates', url_prefix='/events')


@events.route('/home')
def events_home():
    return render_template('events_home.html')
