# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, HiddenField, SelectField
from wtforms.validators import InputRequired
from google.appengine.ext import ndb


class RegisterEventForm(Form):
    fb_url = StringField(render_kw={'placeholder': 'Ingresa la URL de tu evento en Facebook'},
                         validators=[InputRequired()])
    fb_event_id = HiddenField(validators=[InputRequired()])
    fb_user_id = HiddenField(validators=[InputRequired()])
    fb_user_token = HiddenField(validators=[InputRequired()])
    event_name = HiddenField(validators=[InputRequired()])
    event_time = HiddenField(validators=[InputRequired()])
    submit = SubmitField(description='Activar Chelómetro')


class ChooseChelaForm(Form):
    event_id = HiddenField(validators=[InputRequired()])
    user_id = HiddenField(validators=[InputRequired()])
    drink_brand = SelectField(choices=[('Victoria', 'victoria'),
                                       ('Corona', 'corona'),
                                       ('Modelo', 'modelo')],
                              validators=[InputRequired()],
                              coerce=str)
    submit = SubmitField(description='Party Hard')


class EventModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    fb_event_id = ndb.StringProperty(required=True,
                                     indexed=True)
    fb_user_id = ndb.StringProperty(required=True,
                                    indexed=True)
    fb_user_token = ndb.StringProperty(required=True)
    # true when event owner has ordered drinks
    made_request = ndb.BooleanProperty(indexed=True)
    # when the event starts
    event_time = ndb.DateTimeProperty(required=True,
                                      indexed=True)
    event_name = ndb.StringProperty(required=True)


class DrinkConfirmationModel(ndb.Model):
    fb_event_id = ndb.StringProperty(required=True,
                                     indexed=True)
    fb_user_id = ndb.StringProperty(required=True,
                                    indexed=True)
    drink_brand = ndb.StringProperty(required=True)

