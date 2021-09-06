import uuid

class User:
    __first_name = ""
    __last_name = ""
    __username = ""
    __email = ""
    __password = None
    __created = None
    __picture_url = None
    __contact_list = None

    # Constructor
    def __init__(self, first_name, last_name, username, email, password, created, picture_url, contact_list = []):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.created = created
        self.picture_url = picture_url
        self.contact_list = contact_list

    # Properties

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def created(self):
        return self.__created

    @created.setter
    def created(self, value):
        self.__created = value

    @property
    def picture_url(self):
        return self.__picture_url

    @picture_url.setter
    def picture_url(self, value):
        self.__picture_url = value

    @property
    def contact_list(self):
        return self.__contact_list

    @contact_list.setter
    def contact_list(self, value):
        self.__contact_list = value


    # Methods

    # Python Dictionary can be easy read as JSON Object
    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created" : self.created,
            "picture_url": self.picture_url,
            "contact_list" : [contact.serialize() for contact in self.contact_list]
        }


