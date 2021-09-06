"""
Flask_Server App

This script initializes the flask_server by instantiating the flask app and
enabling Cross Origin Resource Sharing.

It contains the following functions for starting the server:

    * configure_app
    * initialize_app
    * main

"""
import logging.config
import datetime
import pymongo
import settings

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_restplus import Api, Namespace, Resource
# from flask_bcrypt import Bcrypt
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)

from api import restplus
from api.webchat.endpoints import user_routes, entry_routes

log = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# MongoDB SetUp
myclient = pymongo.MongoClient("mongodb://terrificdb:27017/")
log.info(">>> Started MongoClient")

mydb = myclient["terrific_tiger_db"]
log.info(">>> Started terrific_tiger_db")

userCollection = mydb["user"]
chatCollection = mydb["chat"]
log.info(">>> Created Collections user and chat!")

def configure_app(flask_app):
    """
        Gets configuration properties from settings.py.

    :param
    flask_app: instantiated flask app
    """
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['MONGODB_DATABASE_NAME'] = settings.MONGODB_DATABASE_NAME
    # flask_app.config['MONGO_URI'] = settings.MONGO_URI
    # flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

    flask_app.config['JWT_SECRET_KEY'] = 'super secret key'
    flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days =1)
    flask_app.config['SESSION_TYPE'] = 'filesystem'

def initialize_app(flask_app):
    """
        Calls the method configure_app and defines initializing attributes with flask_restplus.
        Adds blueprints -- TO DO ---
        Adds namespaces of routes

    :param
    flask_app: instantiated flask app
    """
    configure_app(flask_app)
    jwt = JWTManager(flask_app)

    # mongo = PyMongo(flask_app)
    # flask_bcrypt = Bcrypt(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    restplus.api.init_app(blueprint)
    restplus.api.add_namespace(user_routes.ns)
    restplus.api.add_namespace(entry_routes.ns)
    flask_app.register_blueprint(blueprint)

def main():
    """
        Main function for running the flask server.
    """
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug= settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()

