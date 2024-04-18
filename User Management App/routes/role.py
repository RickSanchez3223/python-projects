from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from forms.create_role import RoleForm
from datetime import datetime
from decorators.auth import session_authentication

roles = Blueprint('roles', __name__)


@roles.route('/create-role', methods=['GET', 'POST'], endpoint='create_role')
@session_authentication(permissions_required=['Admin Access'])
def create_role():
    form = RoleForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form.get('name')
            permissions = request.form.getlist('permissions')

            # Save the role with selected permissions
            role = {'name': name, 'permissions': permissions, 'is_admin': False, 'is_deleted': False, "created_at": datetime.utcnow(), "deleted_at": None}
            from app import mongo
            mongo.db.role.insert_one(role)
            flash('Role created successfully.', 'success')
            return redirect(url_for('user-details.user_list_view'))

    return render_template('create_role.html', form=form, user_role=session['role'])


@roles.route('/delete-role', methods=['GET'])
@session_authentication(permissions_required=['Admin Access'])
def delete_role_view():
    try:
        name = request.args.get('name')
        from app import mongo
        update_data = {
            '$set': {'is_deleted': True, 'deleted_at': datetime.utcnow()}
        }
        # Soft delete
        data = mongo.db.role.update_one({'name': name}, update_data)
        # mongo.db.role.delete_one({"email": email})

        # Soft delete users with this role
        update_data = {
            '$set': {'is_deleted': True, 'deleted_at': datetime.utcnow()}
        }
        mongo.db.user.update_many({'role': name, 'is_admin': False}, update_data)

        if not data:
            return jsonify({'error': 'Bad Request'}), 400
        
        return jsonify({'message': 'Role deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
