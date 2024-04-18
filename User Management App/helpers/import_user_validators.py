from marshmallow import Schema, fields, validates, ValidationError
from constants import APP_ROLES, DEPARTMENTS, DESIGNATIONS


class ManagerCreateSchema(Schema):
    name = fields.String(required=True, validate=lambda s: s.strip() != "")
    phone_number = fields.String(required=True, validate=lambda s: s.strip() != "")
    email = fields.Email(required=True, validate=lambda s: s.strip() != "")
    password = fields.String(required=True, validate=lambda s: s.strip() != "")
    hired_date = fields.String(
        required=True, validate=lambda s: s.strip() != "")
    role = fields.String(required=True, validate=lambda s: s.strip() != "")

    @validates("role")
    def validate_role(self, value):
        if value not in APP_ROLES:
            raise ValidationError(f"Invalid role. Role must be one of {', '.join(APP_ROLES)}")

    @validates("name")
    def validate_name(self, value):
        from app import mongo
        name = value
        user = mongo.db.user.find_one({'name': name, 'is_deleted': False})
        if user:
            raise ValidationError(f'This name {name} is already taken')

    @validates("email")
    def validate_unique_email(self, value):
        from app import mongo
        email = value
        user = mongo.db.user.find_one({'email': email, 'is_deleted': False})
        if user:
            raise ValidationError(f'This email {value} is already taken')


class EmployeeCreateSchema(ManagerCreateSchema):
    designation = fields.String(required=True, validate=lambda s: s.strip() != "")
    department = fields.String(required=True, validate=lambda s: s.strip() != "")
    manager = fields.String(required=True, validate=lambda s: s.strip() != "")

    @validates("manager")
    def validate_manager(self, value):
        from app import mongo
        user = mongo.db.user.find_one({'name': value, 'is_deleted': False, 'role': 'Manager'})
        if not user:
            raise ValidationError(f'This manager {value} is invalid')

    @validates("designation")
    def validate_designation(self, value):
        if value not in DESIGNATIONS:
            raise ValidationError(f"Invalid designation. Designation must be one of {', '.join(DESIGNATIONS)}")

    @validates("department")
    def validate_department(self, value):
        if value not in DEPARTMENTS:
            raise ValidationError(f"Invalid department. Department must be one of {', '.join(DEPARTMENTS)}")
