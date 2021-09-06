"""
Pytest introduces the concept of fixtures.
For instance, a fixture is just a named function, which constructs a test object (e.g. a mock database connection).
Whenever a test function declares a formal parameter whose name coincides with the name of the fixture,
pytest will invoke the corresponding fixture function and pass its result to the test.

"""


import unittest
import os

from app import app

from mockupdb import MockupDB, go, Command
from pymongo import MongoClient
from mockupdb._bson import ObjectId as mockup_oid
from json import dumps


class GetDataSourceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.server = MockupDB(auto_ismaster=True, verbose=True)
        self.server.run()

        # create mongo connection to mock server
        app.testing = True
        app.config['MONGO_URI'] = "mongodb://terrificdb:27017/"
        self.app = app.test_client()

    @classmethod
    def tearDownClass(self):
        self.server.stop()