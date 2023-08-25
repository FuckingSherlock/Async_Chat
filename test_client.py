import unittest
from client import *
import chardet
import json


class TestClass(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestClass, self).__init__(*args, **kwargs)
        self.test_name = 'TEST_username'

    def test_presense(self):
        def dec(name):
            enc = chardet.detect(presence(name))['encoding']
            return json.loads(presence(name).decode(enc))

        self.assertEqual(dec(self.test_name)['user']['account_name'], self.test_name)

    def test_get_server_msg(self):
        self.assertEqual(get_server_msg(presence(self.test_name)))


if __name__ == '__main__':
    unittest.main()
