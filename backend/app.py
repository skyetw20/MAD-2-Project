from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/2'
db = SQLAlchemy(app) 
jwt = JWTManager(app)

# import routes
import models
