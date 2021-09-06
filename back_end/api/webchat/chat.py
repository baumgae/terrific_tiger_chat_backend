import uuid
import datetime

class Chat:

    __chatpartner1ID = None
    __chatpartner2ID = None
    __chatpartner1Name = None
    __chatpartner2Name = None
    __chat_messages = None
    __last_modified = None

    def __init__(self, chatpartner1ID, chatpartner2ID, chatpartner1Name,
                 chatpartner2Name, chat_messages = [], last_modified = datetime):
        self.chatpartner1ID = chatpartner1ID
        self.chatpartner2ID = chatpartner2ID
        self.chatpartner1Name = chatpartner1Name
        self.chatpartner2Name = chatpartner2Name
        self.chat_messages = chat_messages
        self.last_modified = last_modified


    # Properties

    @property
    def chatpartner1ID(self):
        return self.__chatpartner1ID

    @chatpartner1ID.setter
    def chatpartner1ID(self, value):
        self.__chatpartner1ID = value

    @property
    def chatpartner2ID(self):
        return self.__chatpartner2ID

    @chatpartner2ID.setter
    def chatpartner2ID(self, value):
        self.__chatpartner2ID = value

    @property
    def chatpartner1Name(self):
        return self.__chatpartner1Name

    @chatpartner1Name.setter
    def chatpartner1Name(self, value):
        self.__chatpartner1Name = value

    @property
    def chatpartner2Name(self):
        return self.__chatpartner2Name

    @chatpartner2Name.setter
    def chatpartner2Name(self, value):
        self.__chatpartner2Name = value

    @property
    def chat_messages(self):
        return self.__chat_messages

    @chat_messages.setter
    def chat_messages(self, value):
        self.__chat_messages = value

    @property
    def last_modified(self):
        return self.__last_modified

    @last_modified.setter
    def last_modified(self, value):
        self.__last_modified = value 

    # Methods

    def serialize(self):
        return {
            "chatpartner1ID" : self.chatpartner1ID,
            "chatpartner2ID" : self.chatpartner2ID,
            "chatpartner1Name" : self.chatpartner1Name,
            "chatpartner2Name" : self.chatpartner2Name,
            "chat_messages" : [message.serialize() for message in self.chat_messages], #List Comprehension Feature
            "last_modified" : self.last_modified
        }

    def add_message(self, message):
        self.chat_messages.append(message)
