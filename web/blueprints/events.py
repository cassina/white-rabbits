# -*- coding: utf-8 -*-
import datetime

from flask import Blueprint, redirect, url_for, render_template, flash

from web.domain import RegisterEventForm, EventModel


events = Blueprint('events', __name__, template_folder='templates')


@events.route('/register', methods=['POST'])
def register():
    form = RegisterEventForm()

    if not form.validate_on_submit():
        return redirect(url_for('canvas.redirect_to_fb_app'))        

    event = EventModel()
    event.fb_event_id = form.fb_event_id.data
    event.fb_user_id = form.fb_user_id.data
    event.fb_user_token = form.fb_user_token.data
    event.made_request = False
    event.event_time = parse_time(form.event_time.data)
    event.put()
    flash('Thank you for registering your Facebook event!')
    return redirect(url_for('events.dashboard', event_id=event.fb_event_id))


def parse_time(date_string):
    import datetime
    return datetime.datetime.strptime(date_string[:-5], '%Y-%m-%dT%H:%M:%S')


@events.route('/<event_id>/<user_id>')
def user_choose_chelas(event_id, user_id):
    return render_template('choose_chelas.html', event_id=event_id, user_id=user_id)


@events.route('/dashboard/<event_id>')
def dashboard(event_id):
    event = EventModel.query(EventModel.fb_event_id == event_id).get()
    is_value = None
    if event.event_time >= datetime.datetime.now():
        is_value = True
    else:
        is_value = False
    return render_template('events_home.html', event=event, value=is_value)


@events.route('/listen')
def listen():
    # Queries Datastore every minute
    query = EventModel.query()
    q1 = query.filter(EventModel.made_request == False)
    q2 = query.filter(EventModel.created <= datetime.datetime.now())
    event_list = query.fetch()
    return str(event_list)
