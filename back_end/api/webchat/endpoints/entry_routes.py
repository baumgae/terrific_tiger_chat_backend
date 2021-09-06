"""
Entry_Routes

This script provides the flask routes for the landing page,
containing login and registration to the terrific-tiger-chat.

:var ns
        defines the namespace for the entry_routes

:var user_model
        defines the model for the Swagger UI Documentation

It contains the following classes and REST-Methods:
    * class LandingPage
        - get
    * class UserLogin
        - get
    * class UserRegistration
        - post

"""

import logging
import datetime
import uuid


from flask import request, redirect, url_for, jsonify, make_response
from flask_restplus import Resource, fields
from datetime import datetime
from bson.objectid import ObjectId                      # MongoDB IdFormat
from flask_bcrypt import Bcrypt                         # Hashing Password
from bson.json_util import loads, dumps
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity) # Generate JWT Token

from api import restplus
from api.webchat.user import User
from api.webchat.endpoints import user_routes
from app import userCollection, chatCollection

log = logging.getLogger(__name__)

ns = restplus.api.namespace('welcome', description='Authentication for the Terrific-Tiger-Chat!')
registration_model = restplus.api.model("User_Registration", {
    "email": fields.String(required=True, description='Email of user'),
    "password" : fields.String(required=True, description='Password of user'),
    "first_name" : fields.String(required=False, description='First name of user'),
    "last_name" : fields.String(required=False, descpription='Last name of user'),
    "username" : fields.String(required=False, description='Username of user')
})
login_model = restplus.api.model("User_Login", {
    "email": fields.String(required=True, description='Email of user'),
    "password": fields.String(required=True, description='Password of user'),
})

@ns.route('/')
class LandingPage(Resource):

        @ns.response(200, 'Success!')
        @ns.doc('Welcome to Terrific-Tiger-Chat')
        def get(self):
            """
            Landing Page - Welcome!
            """
            result = jsonify({"response": "Welcome to the Terrific-Tiger-Chat!"})
            return result


@ns.route('/login')
class UserLogin(Resource):

    @ns.expect(login_model)
    def post(self):
        """
        Login for user

        :var existing_users
            Test user from database.test_users.py

        :var email, password
            Required fields for login

        :var response
            Searches for matching user in test users

        :returns
            JWT Token, if user exists and password is correct - 200
            MSG, if password is invalid - 403
            MSG, if response did not find user - 404
            MSG, if required property is not given - 400

        """

        login_email = request.get_json()['email']
        login_password = request.get_json()['password']

        # PYMONGO
        response = userCollection.find_one({'email': login_email})
        print(response)

        # PYMONGO
        if response:

            checkpassword = response['password']

            if checkpassword == login_password:

                access_token = create_access_token(identity = {
                    'id' : str(response['_id']),
                    'username' : response['username'],
                    'email' : response['email']
                    })
                token = jsonify(access_token=access_token)
                response = make_response(token, 200)

            else:
                msg = jsonify({"msg": "Invalid Password"})
                response = make_response(msg, 403)

        else:
            msg = jsonify({"msg": "Invalid Email"})
            response = make_response(msg, 404)

        return response


@ns.route('/register')
class UserRegistration(Resource):

    @ns.expect(registration_model)
    def post(self):
        """
        Create and register a new user

        :var existing_users
            Test user from database.test_users.py

        :var first_name, last_name, username, email, password
            Required fields for registration

        :var response
            Searches for matching user in test users

        :returns
            Success and welcome, if user is registred - 200
            MSG, if email already exists - 403
            MSG, if required property is not given - 400
        """

        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        username = request.get_json()['username'].lower()
        email = request.get_json()['email']
        password = request.get_json()['password']
        created = datetime.utcnow()

        # PYMONGO
        registered_user = userCollection.find_one({'email' : email})
        log.info(">>>>>>>>>>>>>Check Output: ", registered_user)

        if registered_user:
            msg = jsonify({"msg": "This Email is already registered!"})
            response = make_response(msg, 403)

        else:
            empty_contacts = []
            empty_picture = ""
            new_user = User(first_name, last_name, username, email, password, created, empty_picture, empty_contacts)
            new_user = new_user.serialize()

            # PYMONGO
            x = userCollection.insert_one(new_user)
            log.info(">>>>>>>>>>>>>x Output: ", x)

            succ = 'Email ' + email + ' is now registered! Welcome to the Terrific-Tiger-Chat!'
            msg = jsonify({"msg": succ})
            response = make_response(msg, 200)

        return response