from flask import request, render_template, Blueprint, redirect, url_for, flash, session
from forms.create_user import CreateEmployeeForm, CreateManagerForm
from decorators.auth import session_authentication
from datetime import datetime
from helpers.generate_employee_id import generate_employee_id
from werkzeug.security import generate_password_hash

from constants import SEARCH_MANAGERS_URL

# Create a Blueprint instance for the 'user-details' module
create_user = Blueprint('create-user', __name__)


CREATE_USER_VIEW_CONFIG = {
    'Employee': {
        "template": "create_employee.html",
        "form": CreateEmployeeForm
        },
    'Manager': {
        "template": "create_manager.html",
        "form": CreateManagerForm
        }
}


@create_user.route('/create-user', methods=['GET', 'POST'], endpoint='create_user_view')
@session_authentication(permissions_required=['Admin Access', 'Add Employee'])
def create_user_view():
    role = request.args.get("role")

    if role in CREATE_USER_VIEW_CONFIG:
        form = CREATE_USER_VIEW_CONFIG[role]['form']()
        template = CREATE_USER_VIEW_CONFIG[role]['template']
    else:
        return "Bad Request. Missing query param", 400

    if request.method == 'POST' and form.validate_on_submit():
        # Retrieve form data
        name = request.form.get('name')
        email = request.form['email']
        phone = request.form.get('phone', '')
        password = request.form.get('password')
        designation = request.form.get('designation', '')
        department = request.form.get('department', '')
        if request.form.get('manager_id'):
            manager = {
                'name': request.form['manager'],
                'id': request.form['manager_id']
            }
        else:
            manager = None
        hired_date = request.form.get('hired_date', None)

        # Insert user into the database
        user_data = {
            "name": name,
            "email": email,
            "password": generate_password_hash(password),
            "role": role,
            "is_admin": False,
            "phone_number": phone,
            "designation": designation,
            "department": department,
            "manager": manager,
            "hired_date": hired_date,
            "is_deleted": False,
            "employee_id": generate_employee_id(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "deleted_at": None
        }

        from app import mongo
        print('GOing to create this user: ', user_data)
        mongo.db.user.insert_one(user_data)
        flash('User created successfully.', 'success')
        return redirect(url_for('user-details.user_details_view', email=email))

    return render_template(template, form=form, user_role=session['role'], SEARCH_MANAGERS_URL=SEARCH_MANAGERS_URL)
