# -*- coding: utf-8 -*-
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
    return redirect(url_for('events.dashboard', event_id=e_id))


def parse_time(date_string):
    import datetime
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')

@events.route('/<event_id>/<user_id>')
def user_choose_chelas(event_id, user_id):
    return render_template('choose_chelas.html', event_id=event_id, user_id=user_id)


@events.route('/dashboard/<event_id>')
def dashboard(event_id):
    return render_template('events_home.html', event_id=event_id)


@events.route('/listen')
def listen():
    event = EventModel.get_by_id(5715999101812736)
    event.fb_user_id += '-A'
    event.put()
    return 'ok'
