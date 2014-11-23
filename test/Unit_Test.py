import unittest
import flask.ext.testing
import urlparse
import redis
from redis import RedisError
from flask import Flask
from flask.ext.testing import TestCase

url = urlparse.urlparse("redis://redistogo:8bc0a4a78f077cca60c78cca6e5a8f1e@dab.redistogo.com:9082/")
redis_control = redis.Redis(host=url.hostname, port=url.port, db=0, password=url.password)

# your test cases
class MyTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_checkServer(self):
        redis_control.ping

    def test_databaseWrite(self):
        
        redis_control.set("Test2","Database Read successfully")
        redis_control.delete("Test2")

    def test_databaseRead(self):
       
        redis_control.get("Test1")
    

if __name__ == '__main__':
    unittest.main()
