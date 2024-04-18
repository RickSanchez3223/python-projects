from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, Email, ValidationError
from wtforms.widgets import HiddenInput
from bson import ObjectId

from constants import MANAGER, DEPARTMENT_CHOICES, DESIGNATION_CHOICES


# Custom validator to check if email is unique in the database
def unique_email(form, field):
    from app import mongo
    email = field.data
    user = mongo.db.user.find_one({'email': email, 'is_deleted': False})
    if user:
        raise ValidationError('This email is already taken')


# Custom validator to check if name is unique in the database
def unique_name(form, field):
    from app import mongo
    name = field.data
    email = form.email.data
    query = {'name': name, 'is_deleted': False}
    if email:
        query['email'] = {'$ne': email}
    user = mongo.db.user.find_one(query)
    if user:
        raise ValidationError('This name is already taken')


# Custom validator to check if manager is valid
def valid_manager(form, field):
    from app import mongo
    manager_id = field.data
    print('VALIDATING MANAGER_ID: ', manager_id)
    if not manager_id:
        raise ValidationError('Invalid manager selection.')
    manager = mongo.db.user.find_one({'_id': ObjectId(manager_id), 'role': MANAGER, 'is_deleted': False})
    print('mager_id: ', manager_id, '  --  ', manager)
    if not manager:
        raise ValidationError('Invalid manager')


class CreateEmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), unique_name])
    email = StringField('Email', validators=[DataRequired(), Email(), unique_email])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    designation = SelectField('Designation', choices=DESIGNATION_CHOICES, validators=[DataRequired()])
    department = SelectField('Department', choices=DEPARTMENT_CHOICES, validators=[DataRequired()])
    manager = StringField('Manager', validators=[DataRequired()])
    hired_date = DateField('Hired Date', format='%Y-%m-%d', validators=[DataRequired()])
    manager_id = StringField('Manager Id',  validators=[DataRequired(), valid_manager], widget=HiddenInput())


class EditEmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), unique_name])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    designation = SelectField('Designation', choices=DESIGNATION_CHOICES, validators=[DataRequired()])
    department = SelectField('Department', choices=DEPARTMENT_CHOICES, validators=[DataRequired()])
    manager = StringField('Manager', validators=[DataRequired()])
    hired_date = DateField('Hired Date', format='%Y-%m-%d', validators=[DataRequired()])
    manager_id = StringField('Manager Id',  validators=[DataRequired(), valid_manager], widget=HiddenInput())


class CreateManagerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), unique_name])
    email = StringField('Email', validators=[DataRequired(), Email(), unique_email])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    hired_date = DateField('Hired Date', format='%Y-%m-%d', validators=[DataRequired()])


class EditManagerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), unique_name])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    hired_date = DateField('Hired Date', format='%Y-%m-%d', validators=[DataRequired()])
