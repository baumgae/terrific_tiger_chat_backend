"""
User Routes

This script provides the flask routes for all operations, an user is able to do.
Containing the following functions

...
"""

import logging
import json
import sys

from flask import request, redirect, url_for, jsonify, make_response
from flask_restplus import Resource, fields
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
# from flask_bcrypt import Bcrypt
from bson import ObjectId

from datetime import datetime

from api import restplus
from api.webchat.message import Message
from api.webchat.chat import Chat
from api.webchat.endpoints import entry_routes
from app import userCollection, chatCollection

log = logging.getLogger(__name__)

# Flask restplus namespace and models
ns = restplus.api.namespace('user', description='Routes and operations related to users and their chat')

settings_model = restplus.api.model("UserSettings", {
    "email": fields.String(required=False, description='Email of user'),
    "password" : fields.String(required=False, description='Password of user'),
    "first_name" : fields.String(required=False, description='First name of user'),
    "last_name" : fields.String(required=False, descpription='Last name of user'),
    "username" : fields.String(required=False, description='Username of user'),
    "image" : fields.String(required=False, description='Picture of user')
})

message_model = restplus.api.model("Message", {
    "authorName" : fields.String(required=False, description='ID of author of message'),
    "content" : fields.String(required=True, description="Content of chat message")
})

chat_model = restplus.api.model("Chat", {
    "chatpartner1ID": fields.String(required=False, description='ID of user'),
    "chatpartner2ID": fields.String(required=False, description='ID of chatpartner'),
    "chatpartner1Name": fields.String(required=False, description='Username of user'),
    "chatpartner2Name": fields.String(required=False, descpription='Username of chatpartner'),
    "chat_messages": fields.String(required=False, description='Array of chat objects'),
    "last_modified": fields.String(required=False, description='Datetime of last modified')
})

delete_model = restplus.api.model("Password", {
    "password" : fields.String(required=True, description='Password of user, for deleting something!')
})

contact_model = restplus.api.model("Contact", {
    "username" : fields.String(required=True, description = 'Username for modifying contacts')
})


def get_user_id():
    jwt_id = get_jwt_identity()
    user_id = ObjectId(jwt_id['id'])
    return user_id

@ns.route('/information')
class InformationMethods(Resource):
    @ns.doc('identity')
    @jwt_required
    def get(self):
        """
        Get User data
        :return identity
        """
        return get_jwt_identity()

@ns.route('/<username>')
class UserMethods(Resource):

    @ns.doc('info')
    @jwt_required
    def get(self, username):
        """
        Get all user information
        :param username:
        :return:
        """
        user_id = get_user_id()
        loggedin_user = userCollection.find_one({'_id' : user_id})

        if loggedin_user:
            user_dict = {}
            user_dict['first_name'] = loggedin_user['first_name']
            user_dict['last_name'] = loggedin_user['last_name']
            user_dict['username'] = loggedin_user['username']
            user_dict['email'] = loggedin_user['email']
            user_dict['picture_url'] = loggedin_user['picture_url']

            user_dict = json.dumps(user_dict)
            response = make_response(user_dict, 200)
        else:
            fail = "You are not allowed to do this action!"
            msg = jsonify({"msg": fail})
            response = make_response(msg, 403)

        return response

    @ns.doc('settings')
    @ns.expect(settings_model)
    @jwt_required
    def post(self, username):
        """
        Change / Update user information
        :param username:
        :returns  200 if it worked, 403 if not
        """
        user_id = get_user_id()
        loggedin_user = userCollection.find_one({'_id' : user_id})
        time = datetime.utcnow()

        update_user = {}

        if loggedin_user:
            new_first_name = request.get_json()['first_name']
            new_last_name = request.get_json()['last_name']
            new_username = request.get_json()['username'].lower()
            new_email = request.get_json()['email']
            new_password = request.get_json()['password']
            new_created = jsonify(time)
            new_picture = request.get_json()['picture_url']

            update_user['_id'] = loggedin_user['_id']
            update_user['first_name'] = new_first_name if new_first_name else loggedin_user['first_name']
            update_user['last_name'] = new_last_name if new_last_name else loggedin_user['last_name']
            update_user['username'] = new_username if new_username else loggedin_user['username']
            update_user['email'] = new_email if new_email else loggedin_user['email']
            update_user['password'] = new_password if new_password else loggedin_user['password']
            update_user['created'] = new_created
            update_user['picture_url'] = new_password if new_picture else loggedin_user['picture_url']
            update_user['contact_list'] = loggedin_user['contact_list']

            update = {'$set': update_user}
            userCollection.update_one({'_id' : user_id}, update)
            update_user = json.dumps(update_user)
            response = make_response(update_user, 200)

        else:
            fail = "You are not allowed to do this action!"
            msg = jsonify({"msg": fail})
            response = make_response(msg, 403)

        return response

    @ns.doc('deleteAccount')
    @ns.expect(delete_model)
    @jwt_required
    def delete(self, username):
        """
        Delete user based on user_id
        :returns 200 if it worked, 403 if not

        """
        # To delete yourself, the user has to type in his password
        password = request.get_json()['password']
        user_id = get_user_id()
        check = userCollection.find_one({'_id': get_user_id()})

        for u in userCollection:
            if u[0] == check:
                if password == check['password']:
                    userCollection.remove(u)
                    succ = "You deleted yourself successfully!"
                    msg = jsonify({"msg": succ})
                    response = make_response(msg, 200)
                else:
                    fail = "Your password is wrong!"
                    msg = jsonify({"msg": fail})
                    response = make_response(msg, 403)
            else:
                fail = "You are not allowed to do this action!"
                msg = jsonify({"msg": fail})
                response = make_response(msg, 403)

        return response


@ns.route('/<username>/contactlist')
class ChatMethods(Resource):

    @ns.doc('friends')
    @jwt_required
    def get(self, username):
        """
        Get chat based of loggedIn User

        :return: contact_list
        """
        user_id = get_user_id()
        check = userCollection.find_one({'_id': user_id})

        if check:
            contacts = check['contact_list']

            # Insert contact information into response
            contact_information = []
            for contact_id in contacts:
                contact_id = ObjectId(contact_id)
                contact = userCollection.find_one({'_id': contact_id})
                contact_id = str(contact['_id'])
                contact_username = contact['username']
                contact_first_name = contact['first_name']
                contact_last_name = contact['last_name']

                user = {'id' : contact_id,
                        'contact_username' : contact_username,
                        'contact_first_name' : contact_first_name,
                        'contact_last_name' : contact_last_name}

                contact_information.append(user)

            result = {"contact_information" : contact_information}
            result = json.dumps(result)
            response = make_response(result, 200)
        else:
            fail = "You are not allowed to do this action!"
            msg = jsonify({"msg": fail})
            response = make_response(msg, 403)

        return response

    @ns.doc('addFriend')
    @ns.expect(contact_model)
    @jwt_required
    def post(self, username):
        """
        Add a new contact to existing contact_list

        :return: modified contact_list
        """
        contact_username = request.get_json()['username']
        user_id = get_user_id()
        loggedIn_user = userCollection.find_one({'_id': user_id})
        find_contact = userCollection.find_one({'username' : contact_username})
        getChatpartnerId = str(find_contact['_id'])

        if loggedIn_user:
            
            if find_contact:
                contacts = loggedIn_user['contact_list']
                contacts_partner = find_contact['contact_list']

                # Check wheter users are already friends
                for item in contacts:
                    if item == getChatpartnerId:
                        fail = "You are already friends!"
                        msg = jsonify({"msg": fail})
                        response = make_response(msg, 404)
                        return response

                # Add new contact to contact_list
                contacts.append(getChatpartnerId)
                new_contacts = {'$set': {'contact_list' : contacts}}
                userCollection.update_one({'_id': user_id}, new_contacts)

                # Add loggedIn User to contact_list of new friend
                contacts_partner.append(str(user_id))
                new_contacts_partner = {'$set': {'contact_list' : contacts_partner}}
                userCollection.update_one({'_id': find_contact['_id']}, new_contacts_partner)

                # Create new chat in chatCollection if not
                chatPartnerID1 = str(user_id)
                chatPartnerID2 = getChatpartnerId
                chatPartnerName1 = loggedIn_user['username']
                chatPartnerName2 = contact_username
                chatMessages = []
                lastModified = datetime.utcnow()

                new_chat = Chat(chatPartnerID1, chatPartnerID2, chatPartnerName1, chatPartnerName2, chatMessages, lastModified)
                new_chat = new_chat.serialize()
                chatCollection.insert_one(new_chat)

                # Return new contact_list
                new_check = userCollection.find_one({'_id': user_id})
                contacts = new_check['contact_list']

                # Insert contact information into response
                contact_information = []
                for contact_id in contacts:
                    contact_id = ObjectId(contact_id)
                    contact = userCollection.find_one({'_id': contact_id})
                    contact_id = str(contact['_id'])
                    contact_username = contact['username']
                    contact_first_name = contact['first_name']
                    contact_last_name = contact['last_name']

                    user = {'id': contact_id,
                            'contact_username': contact_username,
                            'contact_first_name': contact_first_name,
                            'contact_last_name': contact_last_name}

                    contact_information.append(user)

                result = {"contact_information": contact_information}
                result = json.dumps(result)
                response = make_response(result, 200)

            else:
                fail = "User does not exist!"
                msg = jsonify({"msg": fail})
                response = make_response(msg, 404)
        else:
            fail = "You are not allowed to do this action!"
            msg = jsonify({"msg": fail})
            response = make_response(msg, 403)

        return response

    @ns.doc('deleteFriend')
    @ns.expect(contact_model)
    @jwt_required
    def delete(self, username):
        """
        Delete a contact from contact_list
        :return: New contact_list
        """
        contact_username = request.get_json()['username']
        user_id = get_user_id()
        loggedIn_user = userCollection.find_one({'_id': user_id})
        find_contact = userCollection.find_one({'username': contact_username})
        partner_id = str(find_contact['_id'])
        user_id = str(get_user_id())

        if loggedIn_user:
            if find_contact:
                old_contacts = loggedIn_user['contact_list']
                contacts_partner = find_contact['contact_list']

                for item in old_contacts:
                    if item == partner_id :

                        # Delete friend from contact_list
                        new_contact = old_contacts.remove(item)
                        new_contacts = {'$set': {'contact_list': new_contact}}
                        userCollection.update_one({'_id': user_id}, new_contacts)

                    else:
                        fail = "Something went wrong :("
                        msg = jsonify({"msg": fail})
                        response = make_response(msg, 404)

                for item in contacts_partner:
                    if item == user_id:
                        # Delete loggedIn User to contact_list
                        contacts_partner.append(str(user_id))
                        new_contacts_partner = {'$set': {'contact_list': contacts_partner}}
                        userCollection.update_one({'_id': find_contact['_id']}, new_contacts_partner)

                    else:
                        fail = "Something went wrong :("
                        msg = jsonify({"msg": fail})
                        response = make_response(msg, 404)

                # Delete chat from chat collection
                query1 = {'$and': [{'chatpartner1ID': partner_id }, {'chatpartner2ID': user_id}]}
                query2 = {'$and': [{'chatpartner1ID': user_id}, {'chatpartner2ID': partner_id}]}
                find_chat = chatCollection.find_one({'$or': [query1, query2]})

                if find_chat:
                    chatCollection.remove(find_chat)

                else:
                    fail = "Something went wrong :("
                    msg = jsonify({"msg": fail})
                    response = make_response(msg, 404)

        else:
            fail = "You are not allowed to do this action!"
            msg = jsonify({"msg": fail})
            response = make_response(msg, 403)

        return response


@ns.route('/<username>/chats')
class ChatMethods(Resource):

    @ns.doc('/messages')
    @jwt_required
    def get(self, username):
        """
        Get the chat of one specific user!

        :return Whole Chat JSON
        """

        partner_name = request.headers.get('username')
        partner = userCollection.find_one({'username': partner_name})
        partner_id = partner['_id']
        partner_id = str(partner_id)
        user_id = str(get_user_id())

        query1 = {'$and' : [{'chatpartner1ID' : partner_id}, {'chatpartner2ID' : user_id}]}
        query2 = {'$and' : [{'chatpartner1ID' : user_id}, {'chatpartner2ID' : partner_id}]}
        find_chat = chatCollection.find_one({'$or': [query1, query2]})

        if find_chat:
            messages = find_chat['chat_messages']
            result = json.dumps(messages)
            response = make_response(result, 200)

        else:
            fail = "You and " + partner['username'] + " have to be friends. Consider adding this contact!"
            msg = jsonify({"msg": fail})
            response = make_response(msg, 404)

        return response

    @ns.expect(message_model)
    @jwt_required
    def post(self, username):
        """
        Add a message to an existing chat

        :return new chat json
        """

        partner_name = request.headers.get('username')
        author = request.get_json()['authorName']
        created = str(datetime.utcnow())
        content = request.get_json()['content']

        user_id = get_user_id()
        user = userCollection.find_one({'_id': user_id})
        username = user['username']
        user_id = str(user_id)          # for the chat

        partner = userCollection.find_one({'username': partner_name})
        partner_id = str(partner['_id'])
        partner_name = partner['username']

        # Get Chat
        query1 = {'$and': [{'chatpartner1ID': partner_id}, {'chatpartner2ID': user_id}]}
        query2 = {'$and': [{'chatpartner1ID': user_id}, {'chatpartner2ID': partner_id}]}
        find_chat = chatCollection.find_one({'$or': [query1, query2]})

        if find_chat:
            messages = find_chat['chat_messages']
            chat_id = find_chat['_id']

            # Create new MessageObject
            if author == username or author == partner_name:
                new_message = Message(author, created, content)
                serialized = new_message.serialize()
                messages.append(serialized)

                # Find and replace
                new_chat = {'$set': {'chat_messages': messages}}
                chatCollection.update_one({'_id': chat_id}, new_chat)

                # Get and return new chats
                messages = find_chat['chat_messages']
                result = json.dumps(messages)
                response = make_response(result, 200)
                return response

            else:
                fail = author + " is not allowed to write in this chat!"
                msg = jsonify({"msg": fail})
                response = make_response(msg, 403)

        else:
            fail = "You and " + partner_name + " have to be friends. Consider adding this contact!"
            msg = jsonify({"msg": fail})
            response = make_response(msg, 404)

        return response



