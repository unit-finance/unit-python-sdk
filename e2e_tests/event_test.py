import os
import unittest
from datetime import datetime, date, timedelta
from unit import Unit
from unit.models.event import *

class EventE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_list_and_get_events(self):
        event_ids = []
        response = self.client.events.list()
        for e in response.data:
            self.assertTrue("." in e.type)
            event_ids.append(e.id)

        for e in event_ids:
            response = self.client.events.get(e)
            self.assertTrue("." in response.data.type)


if __name__ == '__main__':
    unittest.main()
