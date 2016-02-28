# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, HiddenField
from wtforms.validators import InputRequired
from google.appengine.ext import ndb


class RegisterEventForm(Form):
    fb_url = StringField(description='Please paste de Facebook Event url Here',
                         validators=[InputRequired()])
    fb_user_id = HiddenField(validators=[InputRequired()])
    fb_user_token = HiddenField(validators=[InputRequired()])
    submit = SubmitField()


class EventModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True,
                                   indexed=True)
    fb_event_id = ndb.StringProperty(required=True,
                                     indexed=True)
    fb_user_id = ndb.StringProperty(required=True,
                                    indexed=True)
    fb_user_token = ndb.StringProperty(required=True,
                                    indexed=True)
