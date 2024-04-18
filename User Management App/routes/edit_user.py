from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from forms.create_user import EditEmployeeForm, EditManagerForm
from decorators.auth import session_authentication
from datetime import datetime

from constants import SEARCH_MANAGERS_URL

edit_user = Blueprint('edit_user', __name__)

EDIT_USER_VIEW_CONFIG = {
    'Employee': {
        "template": "edit_employee.html",
        "form": EditEmployeeForm
        },
    'Manager': {
        "template": "edit_manager.html",
        "form": EditManagerForm
        }
}


@edit_user.route('/edit-user', methods=['GET', 'POST'])
@session_authentication(permissions_required=['Admin Access', 'Edit Employee'])
def edit_user_view():
    # Get the email from the query parameter
    email = request.args.get('email')

    if not email:
        email = session['email']

    # Query the database to get the user data by email

    from app import mongo
    user_data = mongo.db.user.find_one({'email': email})
    if user_data:
        # Create a form and populate it with user data
        role = user_data['role']
        if role in EDIT_USER_VIEW_CONFIG:
            form = EDIT_USER_VIEW_CONFIG[role]['form']()
            template = EDIT_USER_VIEW_CONFIG[role]['template']
        else:
            return "Bad Request. This user cannot be edited", 400
        if request.method == 'GET':
            manager_obj = user_data['manager']

            # Update the user data with the form data

            form_fields = form._fields.keys()
            if 'name' in form_fields:
                form.name.data = user_data.get('name', '')
            if 'email' in form_fields:
                form.email.data = user_data.get('email', '')
            if 'phone' in form_fields:
                form.phone.data = user_data.get('phone_number', '')
            if 'designation' in form_fields:
                form.designation.data = user_data.get('designation', '')
            if 'department' in form_fields:
                form.department.data = user_data.get('department', '')
            if 'manager' in form_fields:
                form.manager.data = manager_obj['name'] if manager_obj else ''
            if 'manager_id' in form_fields:
                form.manager_id.data = manager_obj['id'] if manager_obj else ''

            # Convert the date string to a datetime object
            hired_date = datetime.strptime(user_data['hired_date'], "%Y-%m-%d")
            form.hired_date.data = hired_date

        elif request.method == 'POST' and form.validate_on_submit():
            name = request.form.get('name', '')
            email = request.form['email']
            phone = request.form.get('phone')
            designation = request.form.get('designation', '')
            department = request.form.get('department', '')
            hired_date = request.form.get('hired_date', None)
            if request.form.get('manager_id'):
                manager = {
                    'name': request.form['manager'],
                    'id': request.form['manager_id']
                }
            else:
                manager = None

            # Insert user into the database
            new_data = {
                "name": name,
                "role": role,
                "is_admin": False,
                "phone_number": phone,
                "designation": designation,
                "department": department,
                "manager": manager,
                "hired_date": hired_date,
                "updated_at": datetime.utcnow()
            }
            print('Going to update this: ', new_data, ' -- Email: ', email)
            filter = {'email': email}

            # Define the update operation you want to perform
            update_data = {
                '$set': new_data
            }

            # Use update_one to update the first matching document
            user_updated = mongo.db.user.update_one(filter, update_data)

            # update user.manager.name
            if role == 'Manager' and user_updated:
                manager_id = str(mongo.db.user.find_one(filter)['_id'])
                mongo.db.user.update_many({'manager.id': manager_id}, {'$set': {'manager.name': name}})

            flash('User updated successfully.', 'success')
            return redirect(url_for('user-details.user_details_view', email=email))

        return render_template(template, form=form, SEARCH_MANAGERS_URL=SEARCH_MANAGERS_URL, user_role=session['role'])
    else:
        flash('User not found.', 'error')
        return redirect(url_for('user-details.user_list_view'))
