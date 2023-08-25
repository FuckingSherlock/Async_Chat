import unittest
from server import *
import chardet
import json


class TestClass(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestClass, self).__init__(*args, **kwargs)
        self.test_name = 'TEST_username'
        self.client_message = {
            "action": "presence",
            "time": 'time',
            "type": "connection check",
            "user": {
                "account_name": self.test_name,
                "status": "I am here!"}
        }
        self.client_message = json.dumps(self.client_message).encode('utf-8')

    def test_get_client_msg_and_answer(self):
        result = get_client_msg_and_answer(self.client_message)
        result = json.loads(result.decode('utf-8'))
        expected = f"Hellow {self.test_name}, welcome! The connection is fine!"
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
