# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from flask import Blueprint, render_template, redirect

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


events = Blueprint('events', __name__, template_folder='templates')

DEMO_URL = 'https://www.facebook.com/events/1315199878496490'


@events.route('/home', methods=['GET', 'POST'])
def events_home():
    form = RegisterEventForm()
    if form.validate_on_submit():
        event = EventModel()
        event.fb_id = form.fb_url.data.split('events/')[1]
        event.url = form.fb_url.data
        event.owner = 'fake-owner'
        event.put()
        return redirect()
    return render_template('events_home.html', form=form)


@events.route('/dashboard')
def event_dashboard():
    pass


class RegisterEventForm(Form):
    fb_url = StringField(description='Please paste de Facebook Event url Here',
                               validators=[InputRequired()])
    submit = SubmitField()


class EventModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True,
                                   indexed=True)
    url = ndb.StringProperty(required=True,
                                      indexed=True)
    fb_id = ndb.StringProperty(required=True,
                                     indexed=True)
    owner = ndb.StringProperty(required=True,
                               indexed=True)
