from flask import Flask
from flask_pymongo import PyMongo
from routes.login_out import login_logout
from routes.user_details import user_details
from routes.create_user import create_user
from routes.edit_user import edit_user
from routes.delete_user import delete_user
from routes.permission import permissions
from routes.role import roles
from routes.users_import import users_import
from flask_session import Session
from datetime import timedelta
from flask_cors import CORS
from gridfs import GridFS
import os

from dotenv import load_dotenv

from constants import INDEX_URL

# Load environment variables from the .env file
load_dotenv()

app = Flask('__name__')
app.secret_key = os.environ.get('SECRET_KEY')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

# Other configuration values
app.config['SESSION_TYPE'] = os.environ.get('SESSION_TYPE')
app.config['SESSION_PERMANENT'] = os.environ.get('SESSION_PERMANENT')
app.config['SESSION_KEY_PREFIX'] = os.environ.get('SESSION_KEY_PREFIX')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.config['SESSION_COOKIE_NAME'] = os.environ.get('SESSION_COOKIE_NAME')

Session(app)
mongo = PyMongo(app)
grid_fs = GridFS(mongo.db)
CORS(app, resources={
    r"/search_manager": {"origins": INDEX_URL},
    r"/users": {"origins": INDEX_URL}
    })

app.register_blueprint(login_logout)
app.register_blueprint(user_details)
app.register_blueprint(create_user)
app.register_blueprint(edit_user)
app.register_blueprint(delete_user)
app.register_blueprint(permissions)
app.register_blueprint(roles)
app.register_blueprint(users_import)

if __name__ == 'main':
    app.run(debug=True)
