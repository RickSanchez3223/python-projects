from pymongo import MongoClient
from werkzeug.security import generate_password_hash

data = [{'name': 'AdminUser', 'email': 'admin@a.com', 'password': '123', 'role': 'Admin', 'is_admin': True, 'phone_number': '123-456-7890', 'designation': 'Engineer', 'department': 'Development', 'manager': {'id': '65266e4eacc14878b1998f0a', 'name': 'Manager1'}, 'hired_date': '2023-01-15', 'employee_id': 'EMP001', 'is_deleted': False}, {'name': 'user1', 'email': 'user1@example.com', 'password': 'pwd@1', 'role': 'Employee', 'is_admin': False, 'phone_number': '123-456-7890', 'designation': 'Engineer', 'department': 'Development', 'manager': {'id': '65266e4eacc14878b1998f0b', 'name': 'Manager2'}, 'hired_date': '2023-01-15', 'employee_id': 'EMP002', 'is_deleted': False}, {'name': 'user2', 'email': 'user2@example.com', 'password': 'pwd@2', 'role': 'Employee', 'is_admin': False, 'phone_number': '234-567-8901', 'designation': 'Architect', 'department': 'Quality Analysis', 'manager': {'id': '65266e4eacc14878b1998f0c', 'name': 'Manager3'}, 'hired_date': '2023-02-20', 'employee_id': 'EMP003', 'is_deleted': False}, {'name': 'user3', 'email': 'user3@example.com', 'password': 'pwd@3', 'role': 'Employee', 'is_admin': False, 'phone_number': '345-678-9012', 'designation': 'Manager', 'department': 'Business Development', 'manager': {'id': '65266e4eacc14878b1998f0d', 'name': 'Manager4'}, 'hired_date': '2023-03-25', 'employee_id': 'EMP004', 'is_deleted': False}, {'name': 'user4', 'email': 'user4@example.com', 'password': 'pwd@4', 'role': 'Employee', 'is_admin': False, 'phone_number': '456-789-0123', 'designation': 'Director', 'department': 'Human Resource', 'manager': {'id': '65266e4eacc14878b1998f0e', 'name': 'Manager5'}, 'hired_date': '2023-04-30', 'employee_id': 'EMP005', 'is_deleted': False}, {'name': 'user5', 'email': 'user5@example.com', 'password': 'pwd@5', 'role': 'Employee', 'is_admin': False, 'phone_number': '567-890-1234', 'designation': 'Engineer', 'department': 'Development', 'manager': {'id': '65266e4eacc14878b1998f0a', 'name': 'Manager1'}, 'hired_date': '2023-05-05', 'employee_id': 'EMP006', 'is_deleted': False}, {'name': 'user6', 'email': 'user6@example.com', 'password': 'pwd@6', 'role': 'Employee', 'is_admin': False, 'phone_number': '678-901-2345', 'designation': 'Architect', 'department': 'Quality Analysis', 'manager': {'id': '65266e4eacc14878b1998f0b', 'name': 'Manager2'}, 'hired_date': '2023-06-10', 'employee_id': 'EMP007', 'is_deleted': False}, {'name': 'user7', 'email': 'user7@example.com', 'password': 'pwd@7', 'role': 'Employee', 'is_admin': False, 'phone_number': '789-012-3456', 'designation': 'Manager', 'department': 'Business Development', 'manager': {'id': '65266e4eacc14878b1998f0c', 'name': 'Manager3'}, 'hired_date': '2023-07-15', 'employee_id': 'EMP008', 'is_deleted': False}, {'name': 'user8', 'email': 'user8@example.com', 'password': 'pwd@8', 'role': 'Employee', 'is_admin': False, 'phone_number': '890-123-4567', 'designation': 'Director', 'department': 'Human Resource', 'manager': {'id': '65266e4eacc14878b1998f0d', 'name': 'Manager4'}, 'hired_date': '2023-08-20', 'employee_id': 'EMP009', 'is_deleted': False}, {'name': 'user9', 'email': 'user9@example.com', 'password': 'pwd@9', 'role': 'Employee', 'is_admin': False, 'phone_number': '901-234-5678', 'designation': 'Engineer', 'department': 'Development', 'manager': {'id': '65266e4eacc14878b1998f0e', 'name': 'Manager5'}, 'hired_date': '2023-09-25', 'employee_id': 'EMP010', 'is_deleted': False}]

data2 = [
    {
        "name": "Manager1",
        "email": "manager1@example.com",
        "password": "pwd@manager1",
        "role": "Manager",
        "is_admin": False,
        "phone_number": "111-111-1111",
        "designation": "Manager",
        "department": "Human Resource",
        "manager": None,
        "hired_date": "2023-11-01",
        "employee_id": "EMP011",
        "is_deleted": False
    },
    {
        "name": "Manager2",
        "email": "manager2@example.com",
        "password": "pwd@manager2",
        "role": "Manager",
        "is_admin": False,
        "phone_number": "222-222-2222",
        "designation": "Manager",
        "department": "Human Resource",
        "manager": None,
        "hired_date": "2023-11-02",
        "employee_id": "EMP012",
        "is_deleted": False
    },
    {
        "name": "Manager3",
        "email": "manager3@example.com",
        "password": "pwd@manager3",
        "role": "Manager",
        "is_admin": False,
        "phone_number": "333-333-3333",
        "designation": "Manager",
        "department": "Human Resource",
        "manager": None,
        "hired_date": "2023-11-03",
        "employee_id": "EMP013",
        "is_deleted": False
    },
    {
        "name": "Manager4",
        "email": "manager4@example.com",
        "password": "pwd@manager4",
        "role": "Manager",
        "is_admin": False,
        "phone_number": "444-444-4444",
        "designation": "Manager",
        "department": "Human Resource",
        "manager": None,
        "hired_date": "2023-11-04",
        "employee_id": "EMP014",
        "is_deleted": False
    },
    {
        "name": "Manager5",
        "email": "manager5@example.com",
        "password": "pwd@manager5",
        "role": "Manager",
        "is_admin": False,
        "phone_number": "555-555-5555",
        "designation": "Manager",
        "department": "Human Resource",
        "manager": None,
        "hired_date": "2023-11-05",
        "employee_id": "EMP015",
        "is_deleted": False
    }
]

roles = [
    {
        'name': 'Admin',
        'permissions': ['Admin Access'],
        'is_admin': True,
        'is_deleted': False
    },
    {
        'name': 'Manager',
        'permissions': ['Add Employee', 'Edit Employee', 'View Employee', 'Delete Employee'],
        'is_admin': False,
        'is_deleted': False
    },
    {
        'name': 'Employee',
        'permissions': [],
        'is_admin': False,
        'is_deleted': False
    }
]


permissions = [
    {
        'name': 'Admin Access',
        'is_deleted': False
    },
    {
        'name': 'Add Employee',
        'is_deleted': False
    },
    {
        'name': 'Edit Employee',
        'is_deleted': False
    },
    {
        'name': 'Delete Employee',
        'is_deleted': False
    },
    {
        'name': 'View Employee',
        'is_deleted': False
    }
]


client = MongoClient("mongodb://localhost:27017/my_sample_db_1")
db = client["my_sample_db_1"]
collection = db["user"]

for user in data+data2:
    user['password'] = generate_password_hash(user['password'])
    if user['manager']: 
        collection.insert_one(user)

# for role in roles:
#     db["role"].insert_one(role)

# for permission in permissions:
#     db["permission"].insert_one(permission)

print("Scirpt completed")
client.close()
