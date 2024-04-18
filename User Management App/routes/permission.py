from flask import request, render_template, Blueprint, redirect, url_for, flash, jsonify, session
from decorators.auth import session_authentication
from forms.permission import PermissionForm
from datetime import datetime

# Create a Blueprint instance for the 'user-details' module
permissions = Blueprint('permissions', __name__)


@permissions.route('/permissions', methods=['GET', 'POST'], endpoint='manage_permission')
@session_authentication(permissions_required=['Admin Access'])
def manage_permissions_view():
    from app import mongo
    _permissions = mongo.db.permission.find()
    form = PermissionForm(request.form)  

    if request.method == 'POST':
        print('form.validate_on_submit(): ', form.validate_on_submit())
        if form.validate_on_submit():
            # Get the selected permission IDs from the form data
            selected_permissions = request.form.getlist('permissions')
            unselected_permissions = list(set([_permission['name'] for _permission in _permissions]).difference(set(selected_permissions)))
            print('selected_permissions: ', selected_permissions)

            # Update the is_deleted status of permissions based on user selection
            update_data = {
                '$set': {
                    'is_deleted': True,
                    'deleted_at': datetime.utcnow()
                }
            }
            filter_condition = {
                'name': {'$in': unselected_permissions}
            }
            mongo.db.permission.update_many(filter_condition, update_data)

            update_data = {
                '$set': {
                    'is_deleted': False
                }
            }
            filter_condition = {
                'name': {'$in': selected_permissions}
            }
            mongo.db.permission.update_many(filter_condition, update_data)

            print('UNSELECTED: ', unselected_permissions)
            update_operation = {
                '$pull': {
                    'permissions': {
                        '$in': unselected_permissions
                    }
                }
            }
            # Update the roles to remove unselected permissions
            mongo.db.role.update_many({}, update_operation)

            flash('Permissions updated successfully', 'success')
            return redirect(url_for('user-details.user_list_view'))
    return render_template('permission.html', permissions=_permissions, form=form, user_role=session['role'])


@permissions.route('/delete-permission', methods=['GET'])
@session_authentication(permissions_required=['Admin Access'])
def delete_permission_view():
    try:
        name = request.args.get('name')
        from app import mongo
        update_data = {
            '$set': {'is_deleted': True, 'deleted_at': datetime.utcnow()}
        }
        # Soft delete
        data = mongo.db.permission.update_one({'name': name}, update_data)
        # mongo.db.permission.delete_one({"email": email})
        
        if not data:
            return jsonify({'error': 'Bad Request'}), 400

        update_operation = {
            '$pull': {
                'permissions': {
                    '$in': [name]
                }
            }
        }
        # Update the document to remove specified permissions
        mongo.db.role.update_many({}, update_operation)

        return jsonify({'message': 'Permission deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
