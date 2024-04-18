from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from constants import PERMISSIONS_CHOICES


# Custom validator to check if name is unique in the database
def unique_name(form, field):
    from app import mongo
    name = field.data
    role = mongo.db.role.find_one({'name': name, 'is_deleted': False})
    if role:
        raise ValidationError('This name is already taken')


class RoleForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), unique_name])
    permissions = SelectMultipleField('Permissions', coerce=str, validators=[InputRequired()], choices=PERMISSIONS_CHOICES)
    submit = SubmitField('Create')
