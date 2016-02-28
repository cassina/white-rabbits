# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, url_for

from web.domain import RegisterEventForm, EventModel


events = Blueprint('events', __name__, template_folder='templates')


@events.route('/register', methods=['POST'])
def register():
    form = RegisterEventForm()
    if form.validate_on_submit():
        event = EventModel()
        event.fb_event_id = form.fb_url.data.split('events/')[1]
        event.fb_user_id = form.fb_user_id.data
        event.put()
        return redirect(url_for('canvas.home'))

