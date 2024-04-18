from decorators.auth import session_authentication
from flask import request, Blueprint, jsonify

from datetime import datetime

# Create a Blueprint instance for the 'user-details' module
delete_user = Blueprint('delete-user', __name__)


@delete_user.route('/delete-user', methods=['GET'])
@session_authentication(permissions_required=['Admin Access', 'Delete Employee'])
def delete_user_view():
    try:
        email = request.args.get('email')
        print(email, 'here')
        from app import mongo
        manager_data = mongo.db.user.find_one({'email': email, 'is_admin': False})

        print(manager_data, 'here')

        if not manager_data:
            return jsonify({'error': 'User not found'}), 404

        update_data = {
            '$set': {'is_deleted': True, 'deleted_at': datetime.utcnow()}
        }
        # Soft delete
        mongo.db.user.update_one({'email': email, 'is_admin': False}, update_data)
        # mongo.db.user.delete_one({"email": email})

        # Remove manager from user.manager
        mongo.db.user.update_many(
            {'manager.id': str(manager_data['_id'])},
            {'$set': {'manager': None}}
        )

        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
