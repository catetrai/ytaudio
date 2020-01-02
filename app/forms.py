from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from app.models import Channel


class SubscribeForm(FlaskForm):
    channel = StringField('channel', validators=[DataRequired()], render_kw={'placeholder': 'youtube/user/<this>'})
    submit = SubmitField('sub')

    def validate_channel(self, channel):
        if Channel.query.filter_by(name=channel.data).first() is not None:
            raise ValidationError('Already subscribed to {}.'.format(channel))


class UnsubscribeForm(FlaskForm):
    channel = HiddenField('channel')
    submit = SubmitField('unsub')
