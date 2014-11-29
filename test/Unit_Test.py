import sys
import os
#Add TextThem directory to path so we can import TextThem module
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import unittest
import flask.ext.testing
import urlparse
import redis
import TextThem
from redis import RedisError
from flask import Flask
from flask.ext.testing import TestCase

PATH_TO_STATIC = os.path.join(os.path.dirname(__file__), "../static")

url = urlparse.urlparse("redis://redistogo:8bc0a4a78f077cca60c78cca6e5a8f1e@dab.redistogo.com:9082/")
redis_control = redis.Redis(host=url.hostname, port=url.port, db=0, password=url.password)

# your test cases
class MyTest(TestCase):

    def create_app(self):

        app = TextThem.app
        app.config['TESTING'] = True
        return app

    def test_checkServer(self):
       redis_control.ping

    def test_databaseWrite(self):
        redis_control.set("Test2","Database Read successfully")
        redis_control.delete("Test2")

    def test_databaseRead(self):
        redis_control.get("Test1")

    def test_generateMessage(self):
        rv = TextThem.generateMessage()

        #Docstring of generateMessage assure returnvalue is (string, string)
        self.assertEqual(len(rv), 2)
        self.assertTrue(isinstance(rv[0], basestring))
        self.assertTrue(isinstance(rv[1], basestring))

        with open(os.path.join(PATH_TO_STATIC, 'adjectives.txt')) as f:
            adjectives = [word for l in f.readlines() for word in l.split()]
        with open(os.path.join(PATH_TO_STATIC, 'nouns.txt')) as f:
            nouns = [word for l in f.readlines() for word in l.split()]

        self.assertIn(rv[0], adjectives)
        self.assertIn(rv[1], nouns)




if __name__ == '__main__':
    unittest.main()
