import os
import unittest
from datetime import datetime, date, timedelta
from api.unit import Unit
from models.account import *


class AccountE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_create_deposit_account(self):
        request = CreateDepositAccountRequest("checking", {"customer": Relationship("customer","49423")}, {"purpose": "checking"})
        response = self.client.accounts.create(request)
        self.assertTrue(response.data.type == "depositAccount")

    def test_get_account(self):
        response = self.client.accounts.get("49226")
        self.assertTrue(response.data.type == "depositAccount")

    def test_list_accounts(self):
        response = self.client.accounts.list()
        for acc in response.data:
            self.assertTrue(acc.type == "depositAccount")

    def test_limits_account(self):
        response = self.client.accounts.limits("49226")
        self.assertTrue(response.data.type == "limits")

    def test_close_account(self):
        response = self.client.accounts.close_account("49226","Fraud")
        self.assertTrue(response.data.type == "depositAccount")

    def test_reopen_account(self):
        response = self.client.accounts.reopen_account("49226")
        self.assertTrue(response.data.type == "depositAccount")

    def test_update_account(self):
        request = PatchDepositAccountRequest("49226", tags={
            "purpose": "tax",
            "trackUserId": "userId_fe6885b5815463b26f65e71095832bdd916890f7"})
        response = self.client.accounts.update(request)
        self.assertTrue(response.data.type == "depositAccount")


if __name__ == '__main__':
    unittest.main()

