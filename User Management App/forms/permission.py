from flask_wtf import FlaskForm
from wtforms import SubmitField


class PermissionForm(FlaskForm):
    submit = SubmitField('Confirm')
