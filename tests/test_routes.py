import ai_ui
import unittest
import json


class MyTestCase(unittest.TestCase):

    def setUp(self):
        ai_ui.app.testing = True
        self.app = ai_ui.app.test_client()

    def test_home(self):
        result = self.app.get('/')
        assert result.status_code == 200

    def test_postcode(self):
        result = self.app.get('/postcode')
        assert result.status_code == 200

    def test_postcode_goodvalue(self):
        result = self.app.get('/postcode/ex26ga')
        assert result.status_code == 200

    def test_postcode_badvalue(self):
        result = self.app.get('/postcode/po155rr')
        print(result.data)
        assert result.status_code == 200
