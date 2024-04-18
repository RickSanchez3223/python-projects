import os

PERMISSIONS_CHOICES = [
    ('Admin Access', 'Admin Access'),
    ('Manager Access', 'Manager Access'),
    ('Add Employee', 'Add Employee'),
    ('Edit Employee', 'Edit Employee'),
    ('Delete Employee', 'Delete Employee'),
    ('View Employee', 'View Employee')
    ]
DESIGNATIONS = [
    'Engineer', 'Architect', 'Manager', 'Director'
]

DEPARTMENTS = [
    'Development', 'Quality Analysis', 'Business Development', 'Human Resource'
]

ROLES = ['Admin', 'Employee', 'Manager']
APP_ROLES = ['Employee', 'Manager']

MANAGER = 'Manager'
ADMIN = 'Admin'
EMPLOYEE = 'Employee'

DESIGNATION_CHOICES = [('Engineer', 'Engineer'), ('Architect', 'Architect'), ('Manager', 'Manager'), ('Director', 'Director')]

DEPARTMENT_CHOICES = [('Development', 'Development'), ('Quality Analysis', 'Quality Analysis'), ('Business Development', 'Business Development'), ('Human Resource', 'Human Resource')]


INDEX_URL = os.environ.get('INDEX_URL')
USER_LIST_URL = INDEX_URL + '/users'
USER_DETAILS_URL = INDEX_URL + '/user'
SEARCH_MANAGERS_URL = INDEX_URL + '/search-manager'
USERS_EXPORT_URL = USER_LIST_URL + '/export'
USERS_IMPORT_URL = USER_LIST_URL + '/import'
USER_DELETE_URL = INDEX_URL + '/delete-user'
ROLE_DELETE_URL = INDEX_URL + '/delete-role'
PERMISSION_DELETE_URL = INDEX_URL + '/delete-permission'
USER_EDIT_URL = INDEX_URL + '/edit-user'
