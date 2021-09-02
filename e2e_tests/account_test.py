import os
import unittest
from datetime import datetime, date, timedelta
from api.unit import Unit
from models.account import *


class AccountE2eTests(unittest.TestCase):
    def test_create_deposit_account(self):
        token = os.environ.get("token")
        request = CreateDepositAccountRequest( "checking", {"customer": Relationship("customer","49423")}, {"purpose": "checking"})
        client = Unit("https://api.s.unit.sh", token)
        response = client.accounts.create(request)
        self.assertTrue(response.data.type == "depositAccount")

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

    def test_limits_account(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        response = client.accounts.limits("49226")
        self.assertTrue(response.data.type == "limits")

    def test_close_account(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        response = client.accounts.close_account("49226")
        self.assertTrue(response.data.type == "depositAccount")

    def test_reopen_account(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        response = client.accounts.reopen_account("49226")
        self.assertTrue(response.data.type == "depositAccount")

    def test_update_account(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        request = PatchDepositAccountRequest("49226", "checking")
        response = client.accounts.update(request)
        self.assertTrue(response.data.type == "depositAccount")


if __name__ == '__main__':
    unittest.main()

