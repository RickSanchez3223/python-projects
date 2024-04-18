# Function to generate a unique employee ID

def generate_employee_id():
    # You can generate a unique ID based on your requirements
    # For example, you can use a combination of a prefix and a sequential number.
    # Here, we use 'EMP' as a prefix followed by a sequential number.

    from app import mongo

    last_employee = mongo.db.user.find_one(sort=[("employee_id", -1)])
    if last_employee:
        last_id = int(last_employee["employee_id"].split("EMP")[-1])
        new_id = f"EMP{last_id + 1:04d}"
    else:
        new_id = "EMP0001"
    return new_id
