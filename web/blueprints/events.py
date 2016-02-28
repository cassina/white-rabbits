# -*- coding: utf-8 -*-
import datetime
import json
import logging
import requests
from dateutil.parser import parse
import time

from google.appengine.ext import ndb
from flask import Blueprint, redirect, url_for, render_template, flash

from web.domain import RegisterEventForm, EventModel, DrinkConfirmationModel, ChooseChelaForm
from secrets import FB_APP_ID, FB_APP_SECRET

events = Blueprint('events', __name__, template_folder='templates')

FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/v2.5/'


@events.route('/register', methods=['POST'])
def register():
    form = RegisterEventForm()

    if not form.validate_on_submit():
        return redirect(url_for('canvas.redirect_to_fb_app'))        

    found = EventModel.query(EventModel.fb_event_id == form.fb_event_id.data).fetch()
    if len(found) > 0:
        return redirect(url_for('events.dashboard', event_id=event.fb_event_id))

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
    date = parse(date_string)
    return local_to_utc(date)


def local_to_utc(date_time):
    secs = time.mktime(date_time.timetuple())
    struct = time.gmtime(secs)
    return date_time.fromtimestamp(time.mktime(struct))


@events.route('/<event_id>/<user_id>', methods=['POST'])
def user_choose_chelas(event_id, user_id):
    form = ChooseChelaForm(event_id=event_id, user_id=user_id)
    return render_template('choose_chelas.html', form=form)


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
    for event in query_active_events():
        send_attendants_notifications(event)
    return 'ok'


def query_active_events():
    event_list = EventModel.query(ndb.AND(EventModel.event_time >= datetime.datetime.now(),
                                          EventModel.made_request == False)).fetch()
    return event_list


@events.route('/notify/<event_id>/<user_id>')
def send_event_notification(event_id, user_id):
    event = EventModel.query(EventModel.fb_event_id == event_id).get()
    response = send_notification(event, user_id)
    return response.text


def send_notification(event, user_id):
    message = u'@[{author}] invites you to choose your drinks for {event}'.format(author=event.fb_user_id, event=event.event_name)
    href = 'events/{}/{}'.format(event.fb_event_id, user_id)

    notification_url = FACEBOOK_GRAPH_URL + "{user_id}/notifications".format(user_id=user_id)
    data = {
      'debug': 'all',
      'access_token': '{}|{}'.format(FB_APP_ID, FB_APP_SECRET),
      'type': 'generic',
      'template': message[:180],
      'href': href
    }

    return requests.request('POST', notification_url, data=data)


@events.route('/attendants/<event_id>')
def attendants(event_id):
    event = EventModel.query(EventModel.fb_event_id == event_id).get()
    send_attendants_notifications(event)
    return 'ok'


def send_attendants_notifications(event):
    event_id = event.fb_event_id
    response = get_attendants(event_id)
    json_r = json.loads(response.text)

    attending_ids = [user['id'] for user in json_r['data']]
    already_sent = DrinkConfirmationModel.query(DrinkConfirmationModel.fb_event_id == event_id).fetch()
    sent_user_ids = [c.fb_user_id for c in already_sent]
    pending_ids = set(attending_ids) - set(sent_user_ids)

    new_ones = []
    for user_id in pending_ids:
        send_notification(event, user_id=user_id)
        confirmation = DrinkConfirmationModel(fb_event_id=event_id, fb_user_id=user_id)
        new_ones.append(confirmation)

    ndb.put_multi(new_ones)
    return response.text

def get_attendants(event_id):
    data = {'access_token': '{}|{}'.format(FB_APP_ID, FB_APP_SECRET)}
    attendants_url = FACEBOOK_GRAPH_URL + '{id}/attending'.format(id=event_id)
    return requests.request('GET', attendants_url, params=data)
