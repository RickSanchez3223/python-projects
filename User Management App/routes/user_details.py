from flask import jsonify, flash, session, request, Response, make_response

from flask import render_template
from flask import Blueprint
from decorators.auth import session_authentication
from datetime import datetime
from helpers.export import EXPORT_CONFIG
from constants import DEPARTMENTS, DESIGNATIONS, EMPLOYEE, USER_DETAILS_URL, USERS_IMPORT_URL, USERS_EXPORT_URL, ROLE_DELETE_URL, PERMISSION_DELETE_URL, USER_DELETE_URL, USER_EDIT_URL, USER_LIST_URL


# Create a Blueprint instance for the 'user-details' module
user_details = Blueprint('user-details', __name__)


def user_dict(user, role=None):
    data = {
        'Employee': {
            'Name': user['name'],
            'Employee ID': user['employee_id'],
            'Phone': user['phone_number'],
            'Email': user['email'],
            'Manager': user['manager']['name'] if user['manager'] else '',
            'Department': user['department']
        },
        'Manager': {
            'Name': user['name'],
            'Phone': user['phone_number'],
            'Email': user['email'],
        },
        'default': {
            'Name': user['name'],
            'Employee ID': user['employee_id'],
            'Phone': user['phone_number'],
            'Email': user['email'],
            'Role': user['role'],
            'Manager': user['manager']['name'] if user['manager'] else '',
            'Department': user['department'],
            'Designation': user['designation'],
            'Hired Date': user['hired_date']
        }
    }
    return data[role or user['role']]


@user_details.route('/users', endpoint='user_list_view')
@session_authentication(permissions_required=['Admin Access', 'View Employee'])
def user_list_view():
    from app import mongo
    search_query = request.args.get('search')
    designations = request.args.get('designations')
    departments = request.args.get('departments')
    formatted_query_params = {}
    # Fetch all users except Admin users (is_admin=False) and apply filters
    query = {'is_admin': False, 'is_deleted': False}

    if 'Admin Access' not in session['permissions']:
        query['role'] = EMPLOYEE
    if search_query:
        formatted_query_params['search'] = search_query
        query['name'] = {'$regex': f'^{search_query}', '$options': 'i'}
    if designations:
        designations = designations.split(',')
        formatted_query_params['designations'] = designations
        query['designation'] = {'$in': designations}
    if departments:
        departments = departments.split(',')
        formatted_query_params['departments'] = departments
        query['department'] = {'$in': departments}

    print('Formatted Query: ', formatted_query_params)
    users = mongo.db.user.find(query)
    
    # Create a dictionary to store users by role
    users_by_role = {}
    
    for user in users:
        role = user['role']
        if role not in users_by_role:
            users_by_role[role] = []
        users_by_role[role].append(user_dict(user))
    
    permissions = mongo.db.permission.find({'is_deleted': False})

    permissions_dict = []
    for permission in permissions:
        permissions_dict.append(
            {
                'Name': permission['name']
            }
        )

    roles = mongo.db.role.find({'is_deleted': False})

    roles_dict = []
    for role in roles:
        roles_dict.append(
            {
                'Name': role['name'],
                'Permissions': ", ".join(role['permissions'])
            }
        )
    
    return render_template(
        'users.html', users_by_role=users_by_role,
        permissions=permissions_dict, roles=roles_dict,
        user_permissions=session['permissions'], user_role=session['role'],
        query_params=formatted_query_params, designations=DESIGNATIONS,
        departments=DEPARTMENTS, USER_DETAILS_URL=USER_DETAILS_URL,
        USERS_EXPORT_URL=USERS_EXPORT_URL,
        PERMISSION_DELETE_URL=PERMISSION_DELETE_URL,
        ROLE_DELETE_URL=ROLE_DELETE_URL, USER_EDIT_URL=USER_EDIT_URL,
        USER_LIST_URL=USER_LIST_URL, USERS_IMPORT_URL=USERS_IMPORT_URL, 
        USER_DELETE_URL=USER_DELETE_URL)


@user_details.route('/user', endpoint='user_details_view')
@session_authentication()
def user_details_view():
    email = request.args.get('email')
    print("In user details")
    session_email = session['email']
    # if session['role'] auth pending

    if email:
        if {'Admin Access', 'View Employee'}.isdisjoint(session['permissions']):
            # Handle the case where the user doesn't have the required permission
            return "Permission denied", 403
    if not email:
        email = session_email
    from app import mongo
    user = mongo.db.user.find_one({'email': email, 'is_deleted': False})
    if not user:
        flash('User does not exists', 'error')
    return render_template('user_details.html', user=user, user_permissions=session['permissions'], user_role=session['role'])


@user_details.route('/search-manager', methods=['POST'])
@session_authentication(permissions_required=['Admin Access', 'Add Employee', 'Edit Employee'])
def search_manager_view():
    name = request.get_json().get('search')

    from app import mongo
    managers = mongo.db.user.find({'role': 'Manager', 'name': {'$regex': f'^{name}', '$options': 'i'}, 'is_deleted': False})

    # Generate HTML elements for search results
    results_html = ""
    for manager in managers:
        results_html += f'<li class="manager-result" onclick="selectManager(\'{manager["_id"]}\', \'{manager["name"]}\')">{manager["name"]}</li>'
    return jsonify(results_html=results_html)


@user_details.route('/users/export', methods=['GET'], endpoint='user_export_view')
@session_authentication(permissions_required=['Admin Access', 'View Employee'])
def users_export_view():
    export_format = request.args.get('format')
    search_query = request.args.get('search')
    designations = request.args.get('designations')
    departments = request.args.get('departments')
    # Fetch all users except Admin users (is_admin=False) and apply filters
    query = {'is_admin': False, 'is_deleted': False}

    if 'Admin Access' not in session['permissions']:
        query['role'] = EMPLOYEE
    if search_query:
        query['name'] = {'$regex': f'^{search_query}', '$options': 'i'}
    if designations:
        designations = designations.split(',')
        query['designation'] = {'$in': designations}
    if departments:
        departments = departments.split(',')
        query['department'] = {'$in': departments}

    if export_format not in EXPORT_CONFIG.keys():
        return make_response('Bad request. Invalid export format', 400)  # Return a bad request response

    # Generate data
    from app import mongo, grid_fs
    if 'Admin Access' not in session['permissions']:
        query.update({'role': EMPLOYEE})
    print('FQ: ', query)
    users_data = mongo.db.user.find(query)

    data = [user_dict(user_data, 'default') for user_data in users_data]

    # Format the data using the format_function from the EXPORT_CONFIG
    format_function = EXPORT_CONFIG[export_format]['format_function']
    formatted_data = format_function(data)
    formatted_data_bytes = formatted_data.encode('utf-8') if export_format in ['json', 'csv'] else formatted_data

    # Save the exported data to GridFS
    file_id = grid_fs.put(formatted_data_bytes, content_type=EXPORT_CONFIG[export_format]['content_type'])

    export_metadata = mongo.db.file_metadata

    # Store metadata about the exported file
    metadata = {
        'file_id': file_id,
        'name': 'users.' + export_format,
        'type': 'Export',
        'format': export_format,
        'uploaded_at': datetime.now(),
        'content_type': EXPORT_CONFIG[export_format]['content_type']
    }
    export_metadata.insert_one(metadata)

    response = Response(formatted_data, content_type=EXPORT_CONFIG[export_format]['content_type'])
    response.headers['Content-Disposition'] = f'attachment; filename=users.{export_format}'
    return response
