# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, url_for, render_template

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


@events.route('/<event_id>/<user_id>')
def user_choose_chelas(event_id, user_id):
    return render_template('choose_chelas.html', event_id=event_id, user_id=user_id)
