# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, HiddenField
from wtforms.validators import InputRequired
from google.appengine.ext import ndb


class RegisterEventForm(Form):
    fb_url = StringField(description='Please paste de Facebook Event url Here',
                         validators=[InputRequired()])
    fb_event_id = HiddenField(validators=[InputRequired()])
    fb_user_id = HiddenField(validators=[InputRequired()])
    fb_user_token = HiddenField(validators=[InputRequired()])
    event_name = HiddenField(validators=[InputRequired()])
    event_time = HiddenField(validators=[InputRequired()])
    submit = SubmitField()


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

    def to_document(self):
        return search.Document(doc_id=self.key.id(),
                               fields=[search.TextField(name='hook',
                                                        value=self.hook),
                                       search.TextField(name='synopsis',
                                                        value=self.synopsis),
                                       search.TextField(name='title',
                                                        value=self.title),
                                       ])

    @classmethod
    def get_index(cls):
        return search.Index(name=cls.__name__)

    def put(self):
        try:
            self.get_index().put(self.to_document())
        except search.Error:
            # If we cannot index it, save it for a later cron job
            self.needsIndexing = True

        # Now save the model to db
        return super(BookModel, self).put()


class DrinkConfirmationModel(ndb.Model):
    fb_event_id = ndb.StringProperty(required=True,
                                     indexed=True)
    fb_user_id = ndb.StringProperty(required=True,
                                    indexed=True)
    drink_brand = ndb.StringProperty(required=True)
    drink_decision = ndb.BooleanProperty(required=True, indexed=True)
