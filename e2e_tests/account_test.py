import os
import unittest
from datetime import datetime, date, timedelta
from api.unit import Unit
from models.account import *


class AccountE2eTests(unittest.TestCase):
    def test_get_account(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        response = client.accounts.get("49226")
        self.assertTrue(response.data.type == "depositAccount")

    def test_list_accounts(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        response = client.accounts.list()
        for acc in response.data:
            self.assertTrue(acc.type == "depositAccount")


if __name__ == '__main__':
    unittest.main()