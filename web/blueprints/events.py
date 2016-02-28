# -*- coding: utf-8 -*-
import datetime
import json
import logging
import requests

from google.appengine.ext import ndb
from flask import Blueprint, redirect, url_for, render_template, flash

from web.domain import RegisterEventForm, EventModel
from secrets import FB_APP_ID, FB_APP_SECRET

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
    event.event_name = form.event_name.data
    event.event_time = parse_time(form.event_time.data)
    event.put()
    flash('Thank you for registering your Facebook event!')
    return redirect(url_for('events.dashboard', event_id=event.fb_event_id))


def parse_time(date_string):
    from dateutil.parser import parse
    date = parse(date_string)
    return local_to_utc(date)

def local_to_utc(datetime):
    secs = time.mktime(datetime.timetuple())
    return time.gmtime(secs)

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
    event_list = EventModel.query(ndb.AND(EventModel.event_time >= datetime.datetime.now(),
                                          EventModel.made_request == False)).fetch()
    event_json = json(str(event_list))
    return event_json


@events.route('/notify/<event_id>/<user_id>')
def send_event_notification(event_id, user_id):
    event = EventModel.query(EventModel.fb_event_id == '1051962044842399').get()
    response = send_notification(event, user_id)
    return response.text


def send_notification(event, user_id):
    message = '@[{author}] invites you to choose your drinks for {event}'.format(author=event.fb_user_id, event=event.event_name)

    href = 'events/{}/{}'.format(event.fb_event_id, user_id)

    notification_url = "https://graph.facebook.com/v2.5/{user_id}/notifications".format(user_id=user_id)
    data = {
      'debug': 'all',
      'access_token': '{}|{}'.format(FB_APP_ID, FB_APP_SECRET),
      'type': 'generic',
      'template': message[:180],
      'href': href
    }

    logging.critical(json.dumps({
        'url': notification_url,
        'data': data
    }))

    return requests.request('POST', notification_url, data=data)
