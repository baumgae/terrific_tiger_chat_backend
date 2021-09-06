
class mongoSetUp:

    def __init__(self, myCient, mydb, userCollection, chatCollection ):
        self.myClient = myCient
        self.mydb = mydb
        self.userCollection = userCollection
        self.chatCollection = chatCollection

    # Get
    @property
    def mydb(self):
        return self.mydb

    @property
    def userCol(self):
        return self.userCollection

    @property
    def chatCol(self):
        return self.chatCollection