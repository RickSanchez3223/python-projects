from flask import jsonify, request

from flask import Blueprint
from datetime import datetime
from helpers.export import EXPORT_CONFIG, validate_data
from decorators.auth import session_authentication


users_import = Blueprint('users-import', __name__)


@users_import.route('/users/import', methods=['POST'])
@session_authentication(permissions_required=['Admin Access'])
def users_import_view():
    # Check if the 'file' field is in the POST request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check if the file was not selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file has an allowed extension (e.g., csv, json, xlsx)
    allowed_extensions = EXPORT_CONFIG.keys()
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    if file_extension not in allowed_extensions:
        return jsonify({'error': 'Invalid file format'}), 400

    file_data = EXPORT_CONFIG[file_extension]['read_function'](file)

    validated_data = validate_data(file_data)
    if validated_data.get("errors"):
        print(validated_data)
        return jsonify({'error': 'Validation failed. ' + str(validated_data['errors'])}), 400
    validated_data = validated_data['data']

    from app import mongo, grid_fs
    mongo.db.user.insert_many(validated_data)
    print('DB write completed')

    # Save the exported data to GridFS
    file_id = grid_fs.put(file, content_type=file.content_type)

    export_metadata = mongo.db.file_metadata

    # Store metadata about the exported file
    metadata = {
        'file_id': file_id,
        'name': 'users.' + file_extension,
        'type': 'Import',
        'format': file_extension,
        'uploaded_at': datetime.now(),
        'content_type': file.content_type
    }
    export_metadata.insert_one(metadata)
    print('File SAVED!!')

    return jsonify({'message': 'Import successful'}), 200
