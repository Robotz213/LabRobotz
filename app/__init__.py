from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import os
from typing import Type
import logging
import dotenv
import os

dotenv.load_dotenv()
    
app = Flask(__name__)

env_vars = {key: os.getenv(key) for key in os.environ}
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{ env_vars["DBLogin"] }:{ env_vars["DBPassword"] }@{ env_vars["DBHost"] }/{ env_vars["Database"] }'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   
app.config['PREFERRED_URL_SCHEME'] = "https"
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config["JWT_SECRET_KEY"] = "super-secret"

db = SQLAlchemy(app)
jwt = JWTManager(app)

from app import routes
