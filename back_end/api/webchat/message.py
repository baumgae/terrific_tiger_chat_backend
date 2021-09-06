import datetime

class Message:

    __authorName = ""
    __created = None
    __content = ""

    def __init__(self, authorName, created = datetime, content = str):
        self.authorName = authorName
        self.created = created
        self.content = content

    # Properties

    @property
    def authorName(self):
        return self.__authorName

    @authorName.setter
    def authorName(self, value):
        self.__authorName = value

    @property
    def created(self):
        return self.__created

    @created.setter
    def created(self, value):
        self.__created = value

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # methods
    def serialize(self):
        return {
            "authorName" : self.authorName,
            "created" : self.created,
            "content" : self.content
        }
