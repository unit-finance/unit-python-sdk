import os
import unittest
from datetime import datetime, date, timedelta
from api.unit import Unit
from models.event import *

class EventE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_list_events(self):
        response = self.client.events.list()
        for t in response.data:
            self.assertTrue("." in t.type)

if __name__ == '__main__':
    unittest.main()
