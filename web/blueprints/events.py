# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from flask import Blueprint, render_template, request

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


events = Blueprint('events', __name__, template_folder='templates', url_prefix='/events')


@events.route('/home', methods=['GET', 'POST'])
def events_home():
    form = RegisterEventForm()
    if form.validate_on_submit():
        event = EventModel()
        event.fb_event_id = 'fake'
        event.fb_event_url = 'fake'
        event.owner = 'fake'
        event.put()
        return 'Event created'
    return render_template('events_home.html', form=form)


class RegisterEventForm(Form):
    fb_event_url = StringField(description='Please paste de Facebook Event url Here',
                               validators=[InputRequired()])
    submit = SubmitField()


class EventModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True,
                                   indexed=True)
    fb_event_url = ndb.StringProperty(required=True,
                                      indexed=True)
    fb_event_id = ndb.StringProperty(required=True,
                                     indexed=True)
    owner = ndb.StringProperty(required=True,
                               indexed=True)
