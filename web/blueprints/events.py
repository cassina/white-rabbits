# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, url_for, render_template, flash
from google.appengine.ext import ndb

from web.domain import RegisterEventForm, EventModel


events = Blueprint('events', __name__, template_folder='templates')


@events.route('/register', methods=['POST'])
def register():
    form = RegisterEventForm()
    if form.validate_on_submit():
        e_id = form.fb_url.data.split('events/')[1]
        event = EventModel()
        event.fb_event_id = e_id
        event.fb_user_id = form.fb_user_id.data
        event.fb_user_token = form.fb_user_token.data
        new_key = event.put()
        flash('Thank you for registering your Facebook event!')
        return redirect(url_for('events.dashboard', event_id=e_id))


@events.route('/<event_id>/<user_id>')
def user_choose_chelas(event_id, user_id):
    return render_template('choose_chelas.html', event_id=event_id, user_id=user_id)


@events.route('/dashboard/<event_id>')
def dashboard(event_id):
    return render_template('events_home.html', event_id=event_id)
